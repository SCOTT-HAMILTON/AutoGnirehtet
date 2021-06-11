{ pkgs ? import <nixpkgs> {} }:
let
  customPython = with pkgs; python38.buildEnv.override {
    extraLibs = with python38Packages; [ pexpect ];
  };
in
with pkgs; mkShell {
  buildInputs = [ customPython gnirehtet ];
  shellHook = ''
    run(){
      python AutoGnirehtet/autognirehtet.py
    }
  '';
}

