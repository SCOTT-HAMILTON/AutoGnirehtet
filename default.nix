{ lib
, buildPythonApplication
, gitignoreSource
, pexpect
}:

buildPythonApplication rec {
  pname = "AutoGnirehtet";
  version = "unstable";

  src = gitignoreSource [] ./.;
  propagatedBuildInputs = [ pexpect ];
  doCheck = false;

  meta = with lib; {
    description = "Automatic reconnect script for gnirehtet";
    license = licenses.mit;
    maintainers = [ "Scott Hamilton <sgn.hamilton+nixpkgs@protonmail.com>" ];
    platforms = platforms.linux;
  };
}
