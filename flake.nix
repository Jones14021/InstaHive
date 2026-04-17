{
  description = "InstaHive Instagram downloader";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonPackages = ps: [
            (pkgs.python3.pkgs.toPythonModule pkgs.instaloader)
            ps.colorama
            ps.tqdm
            ps.requests
            ps.psutil
          ];
          python = pkgs.python3.withPackages pythonPackages;
        in
        {
          default = pkgs.writeShellApplication {
            name = "instahive";
            runtimeInputs = [ python ];
            text = ''
              exec ${python}/bin/python ${./instagram_downloader.py} "$@"
            '';
          };
        });

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/instahive";
        };
      });

      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          pythonPackages = ps: [
            (pkgs.python3.pkgs.toPythonModule pkgs.instaloader)
            ps.colorama
            ps.tqdm
            ps.requests
            ps.psutil
          ];
        in
        {
          default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages pythonPackages)
            ];
          };
        });
    };
}
