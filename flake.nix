{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs:
    inputs.flake-utils.lib.eachSystem ["x86_64-linux"] (system: let
      config = {
        allowUnfree = true;
        # cudaSupport = true;
      };

      overlay-unstable = final: prev: {
        unstable = import inputs.nixpkgs-unstable {
          inherit system config;
        };
      };
      pkgs = import inputs.nixpkgs {
        inherit system config;
        overlays = [
          overlay-unstable
        ];
      };

      fhs = pkgs.buildFHSEnv {
        name = "fhs-shell";
        targetPkgs = p: (packages p) ++ custom-commands;
        runScript = "${pkgs.zsh}/bin/zsh";
        profile = ''
          export FHS=1
          source ./.venv/bin/activate
          source .env
        '';
      };
      chatmed-kube-setup = pkgs.writeShellScriptBin "chatmed-kube-setup" ''
          #!/usr/bin/env bash

          # - [Question: does skaffold support Minikube with podman? · Issue #9194 · GoogleContainerTools/skaffold · GitHub](https://github.com/GoogleContainerTools/skaffold/issues/9194)
          # skaffold only supports docker rn
          # - [podman | minikube](https://minikube.sigs.k8s.io/docs/drivers/podman/)
          # minikube config set rootless true
          # minikube start --driver=podman --container-runtime=containerd
          minikube start
          # kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
          minikube addons enable ingress
          minikube addons enable ingress-dns
      '';
      chatmed-kube-serve = pkgs.writeShellScriptBin "chatmed-kube-serve" ''
          #!/usr/bin/env bash
          skaffold dev

          # skaffold dev &
          # sleep 5
          # kubectl port-forward "$(kubectl get pods | grep query-preprocessing | cut -d ' ' -f1)" 9898:80
          # kubectl port-forward development/query-preprocessing-development 9898:80
      '';
      chatmed-kube-stop = pkgs.writeShellScriptBin "chatmed-kube-stop" ''
          #!/usr/bin/env bash
          minikube stop
      '';

      custom-commands = [
        chatmed-kube-setup
        chatmed-kube-serve
        chatmed-kube-stop
      ];

      packages = pkgs: (with pkgs; [
        (pkgs.python310.withPackages (ps:
          with ps; [
          ]))
        python311Packages.python-lsp-server
        python311Packages.ruff-lsp # python linter
        python311Packages.black # python formatter

        pkgs.python310Packages.pip
        pkgs.python310Packages.virtualenv
        zlib # idk why/if this is needed

        redis
        kubernetes
        skaffold
        minikube
        nodejs_21

        # virtualenv .venv
        # source ./.venv/bin/activate
        # pip install ..
        # python311Packages.venvShellHook # ??
      ]);
    in {
      devShells.default = pkgs.mkShell {
        nativeBuildInputs = [fhs] ++ custom-commands ++ packages pkgs;
        shellHook = ''
          source .env
        '';
      };
      # devShells.default = fhs.env;
    });
}
