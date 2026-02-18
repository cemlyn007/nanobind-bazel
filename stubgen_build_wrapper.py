import argparse
from pathlib import Path

from stubgen import main


def _module_name_from_path(module_file: Path) -> tuple[str, str]:
    parts = module_file.parts
    try:
        bin_index = parts.index("bin")
    except ValueError as exc:
        raise ValueError(
            f"Could not infer Bazel bin/ root from module path: {module_file}"
        ) from exc

    bindir = str(Path(*parts[: bin_index + 1]))
    relative = Path(*parts[bin_index + 1 :])
    module_without_ext = relative.with_name(relative.with_suffix("").stem)
    module_name = ".".join(module_without_ext.parts)
    return bindir, module_name


def run() -> None:
    parser = argparse.ArgumentParser(description="Build-time nanobind stubgen wrapper")
    parser.add_argument("--module-file", required=True)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    bindir, module_name = _module_name_from_path(Path(args.module_file))

    stubgen_args = [
        "-i",
        bindir,
        "-m",
        module_name,
        "-o",
        args.output_file,
    ]
    if args.quiet:
        stubgen_args.append("-q")

    main(stubgen_args)


if __name__ == "__main__":
    run()
