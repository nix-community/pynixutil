let
  pkgs = import <nixpkgs> { };
  inherit (pkgs) poetry2nix;

  pythonEnv = poetry2nix.mkPoetryEnv { projectDir = ./.; };

in
pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pythonEnv
    pkgs.nix  # Use a stable release of Nix for testing regardless of system install
  ];
}
