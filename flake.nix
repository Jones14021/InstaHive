{
  description = "InstaHive Instagram downloader";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f system);
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python3.withPackages (ps: with ps; [
            instaloader
            colorama
            tqdm
            requests
            psutil
          ]);
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
    };
}
