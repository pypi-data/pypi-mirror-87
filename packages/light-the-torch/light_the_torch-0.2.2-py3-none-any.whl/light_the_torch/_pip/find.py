import re
from typing import Any, Iterable, List, NoReturn, Optional, Text, Tuple, Union, cast

from pip._internal.index.collector import LinkCollector
from pip._internal.index.package_finder import (
    CandidateEvaluator,
    CandidatePreferences,
    LinkEvaluator,
    PackageFinder,
)
from pip._internal.models.candidate import InstallationCandidate
from pip._internal.models.link import Link
from pip._internal.models.search_scope import SearchScope
from pip._internal.req.req_install import InstallRequirement
from pip._internal.req.req_set import RequirementSet

from ..computation_backend import ComputationBackend, detect_computation_backend
from .common import (
    InternalLTTError,
    PatchedInstallCommand,
    PatchedResolverBase,
    new_from_similar,
    run,
)
from .extract import extract_dists

__all__ = ["find_links"]


def find_links(
    pip_install_args: List[str],
    computation_backend: Optional[Union[str, ComputationBackend]] = None,
    platform: Optional[str] = None,
    python_version: Optional[str] = None,
    verbose: bool = False,
) -> List[str]:
    """Find wheel links for direct or indirect PyTorch distributions with given
    properties.

    Args:
        pip_install_args: Arguments passed to ``pip install`` that will be searched for
            required PyTorch distributions
        computation_backend: Computation backend, for example ``"cpu"`` or ``"cu102"``.
            Defaults to the available hardware of the running system preferring CUDA
            over CPU.
        platform: Platform, for example ``"linux_x86_64"`` or ``"win_amd64"``. Defaults
            to the platform of the running system.
        python_version: Python version, for example ``"3"`` or ``"3.7"``. Defaults to
            the version of the running interpreter.
        verbose: If ``True``, print additional information to STDOUT.

    Returns:
        Wheel links with given properties for all required PyTorch distributions.
    """
    if isinstance(computation_backend, str):
        computation_backend = ComputationBackend.from_str(computation_backend)

    dists = extract_dists(pip_install_args)

    cmd = StopAfterPytorchLinksFoundCommand(computation_backend=computation_backend)
    pip_install_args = adjust_pip_install_args(dists, platform, python_version)
    options, args = cmd.parser.parse_args(pip_install_args)
    try:
        run(cmd, args, options, verbose)
    except PytorchLinksFound as resolution:
        return resolution.links
    else:
        raise InternalLTTError


def adjust_pip_install_args(
    pip_install_args: List[str], platform: Optional[str], python_version: Optional[str]
) -> List[str]:
    if platform is None and python_version is None:
        return pip_install_args

    if platform is not None:
        pip_install_args = maybe_add_option(
            pip_install_args, "--platform", value=platform
        )
    if python_version is not None:
        pip_install_args = maybe_add_option(
            pip_install_args, "--python-version", value=python_version
        )
    return maybe_set_required_options(pip_install_args)


def maybe_add_option(
    args: List[str],
    option: str,
    value: Optional[str] = None,
    aliases: Iterable[str] = (),
) -> List[str]:
    if any(arg in args for arg in (option, *aliases)):
        return args

    additional_args = [option]
    if value is not None:
        additional_args.append(value)
    return additional_args + args


def maybe_set_required_options(pip_install_args: List[str]) -> List[str]:
    pip_install_args = maybe_add_option(
        pip_install_args, "-t", value=".", aliases=("--target",)
    )
    pip_install_args = maybe_add_option(
        pip_install_args, "--only-binary", value=":all:"
    )
    return pip_install_args


class PytorchLinksFound(RuntimeError):
    def __init__(self, links: List[str]) -> None:
        self.links = links


class PytorchLinkEvaluator(LinkEvaluator):
    HAS_LOCAL_PATTERN = re.compile(r"[+](cpu|cu\d+)$")
    EXTRACT_LOCAL_PATTERN = re.compile(r"^/whl/(?P<local_specifier>(cpu|cu\d+))")

    @classmethod
    def from_link_evaluator(
        cls, link_evaluator: LinkEvaluator
    ) -> "PytorchLinkEvaluator":
        return new_from_similar(
            cls,
            link_evaluator,
            (
                "project_name",
                "canonical_name",
                "formats",
                "target_python",
                "allow_yanked",
                "ignore_requires_python",
            ),
        )

    def evaluate_link(self, link: Link) -> Tuple[bool, Optional[Text]]:
        output = cast(Tuple[bool, Optional[Text]], super().evaluate_link(link))
        is_candidate, result = output
        if not is_candidate:
            return output

        result = cast(Text, result)
        has_local = self.HAS_LOCAL_PATTERN.search(result) is not None
        if has_local:
            return output

        return True, f"{result}+{self.extract_computation_backend_from_link(link)}"

    def extract_computation_backend_from_link(self, link: Link) -> Optional[str]:
        match = self.EXTRACT_LOCAL_PATTERN.match(link.path)
        if match is None:
            return "any"

        return match.group("local_specifier")


class PytorchCandidatePreferences(CandidatePreferences):
    def __init__(
        self,
        *args: Any,
        computation_backend: Optional[ComputationBackend] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        if computation_backend is None:
            computation_backend = detect_computation_backend()
        self.computation_backend = computation_backend

    @classmethod
    def from_candidate_preferences(
        cls,
        candidate_preferences: CandidatePreferences,
        computation_backend: Optional[ComputationBackend] = None,
    ) -> "PytorchCandidatePreferences":
        return new_from_similar(
            cls,
            candidate_preferences,
            ("prefer_binary", "allow_all_prereleases",),
            computation_backend=computation_backend,
        )


class PytorchCandidateEvaluator(CandidateEvaluator):
    def __init__(
        self,
        *args: Any,
        computation_backend: Optional[ComputationBackend] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.computation_backend = computation_backend

    @classmethod
    def from_candidate_evaluator(
        cls,
        candidate_evaluator: CandidateEvaluator,
        computation_backend: Optional[ComputationBackend] = None,
    ) -> "PytorchCandidateEvaluator":
        return new_from_similar(
            cls,
            candidate_evaluator,
            (
                "project_name",
                "supported_tags",
                "specifier",
                "prefer_binary",
                "allow_all_prereleases",
                "hashes",
            ),
            computation_backend=computation_backend,
        )

    def get_applicable_candidates(
        self, candidates: List[InstallationCandidate]
    ) -> List[InstallationCandidate]:
        return [
            candidate
            for candidate in super().get_applicable_candidates(candidates)
            if candidate.version.local == "any"
            or candidate.version.local == self.computation_backend
        ]


class PytorchLinkCollector(LinkCollector):
    def __init__(
        self,
        *args: Any,
        url: str = "https://download.pytorch.org/whl/torch_stable.html",
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.search_scope = SearchScope.create(find_links=[url], index_urls=[])

    @classmethod
    def from_link_collector(
        cls, link_collector: LinkCollector
    ) -> "PytorchLinkCollector":
        return new_from_similar(cls, link_collector, ("session", "search_scope",),)


class PytorchPackageFinder(PackageFinder):
    _candidate_prefs: PytorchCandidatePreferences
    _link_collector: PytorchLinkCollector

    def __init__(
        self,
        *args: Any,
        computation_backend: Optional[ComputationBackend] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._candidate_prefs = PytorchCandidatePreferences.from_candidate_preferences(
            self._candidate_prefs, computation_backend=computation_backend
        )
        self._link_collector = PytorchLinkCollector.from_link_collector(
            self._link_collector
        )

    def make_candidate_evaluator(
        self, *args: Any, **kwargs: Any,
    ) -> PytorchCandidateEvaluator:
        candidate_evaluator = super().make_candidate_evaluator(*args, **kwargs)
        return PytorchCandidateEvaluator.from_candidate_evaluator(
            candidate_evaluator,
            computation_backend=self._candidate_prefs.computation_backend,
        )

    def make_link_evaluator(self, *args: Any, **kwargs: Any) -> PytorchLinkEvaluator:
        link_evaluator = super().make_link_evaluator(*args, **kwargs)
        return PytorchLinkEvaluator.from_link_evaluator(link_evaluator)

    @classmethod
    def from_package_finder(
        cls,
        package_finder: PackageFinder,
        computation_backend: Optional[ComputationBackend] = None,
    ) -> "PytorchPackageFinder":
        return new_from_similar(
            cls,
            package_finder,
            (
                "link_collector",
                "target_python",
                "allow_yanked",
                "format_control",
                "candidate_prefs",
                "ignore_requires_python",
            ),
            computation_backend=computation_backend,
        )


class StopAfterPytorchLinksFoundResolver(PatchedResolverBase):
    def _resolve_one(
        self, requirement_set: RequirementSet, req_to_install: InstallRequirement
    ) -> List[InstallRequirement]:
        self._populate_link(req_to_install)
        return []

    def resolve(
        self, root_reqs: List[InstallRequirement], check_supported_wheels: bool
    ) -> NoReturn:
        requirement_set = super().resolve(root_reqs, check_supported_wheels)
        links = [req.link.url for req in requirement_set.all_requirements]
        raise PytorchLinksFound(links)


class StopAfterPytorchLinksFoundCommand(PatchedInstallCommand):
    def __init__(
        self, computation_backend: Optional[ComputationBackend] = None, **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.computation_backend = computation_backend

    def _build_package_finder(self, *args: Any, **kwargs: Any) -> PytorchPackageFinder:
        package_finder = super()._build_package_finder(*args, **kwargs)
        return PytorchPackageFinder.from_package_finder(
            package_finder, computation_backend=self.computation_backend
        )

    def make_resolver(
        self, *args: Any, **kwargs: Any
    ) -> StopAfterPytorchLinksFoundResolver:
        resolver = super().make_resolver(*args, **kwargs)
        return StopAfterPytorchLinksFoundResolver.from_resolver(resolver)
