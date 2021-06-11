{ pkgs ? import <nixpkgs> {} }:
let
  # customPython = with pkgs; python38.buildEnv.override {
  #   extraLibs = with python38Packages; [ pexpect ];
  # };
  autognirehtet = with pkgs.python38Packages; callPackage ./. {
    inherit (pkgs.nix-gitignore) gitignoreSource;
  };
in
with pkgs; mkShell {
  buildInputs = [ autognirehtet gnirehtet ];
  shellHook = ''
    run(){
      # python AutoGnirehtet/autognirehtet.py
      auto-gnirehtet
    }
  '';
}

