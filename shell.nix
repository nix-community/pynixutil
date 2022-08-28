let
  pkgs = import <nixpkgs> { };
  inherit (pkgs) poetry2nix;

  python = pkgs.python39;

  pythonEnv = poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    inherit python;
  };

in
pkgs.mkShell {
  buildInputs = [
    python
    (pkgs.poetry.override { inherit python; })
    pythonEnv
    pkgs.nix  # Use a stable release of Nix for testing regardless of system install
  ];
}
