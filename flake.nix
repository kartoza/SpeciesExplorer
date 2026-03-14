# SPDX-FileCopyrightText: Tim Sutton
# SPDX-License-Identifier: MIT
{
  description = "SpeciesExplorer - QGIS plugin for exploring species occurrence data from GBIF";

  inputs = {
    qgis-upstream.url = "github:qgis/qgis";
    geospatial.url = "github:imincik/geospatial-nix.repo";
    nixpkgs.follows = "geospatial/nixpkgs";
  };

  outputs =
    {
      self,
      qgis-upstream,
      geospatial,
      nixpkgs,
    }:
    let
      system = "x86_64-linux";
      profileName = "SpeciesExplorer";
      pluginName = "SpeciesExplorer";

      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };

      # Extra Python packages for QGIS
      extraPythonPackages = ps: [
        ps.jsonschema
        ps.debugpy
        ps.psutil
        ps.httpx
        ps.requests
      ];

      # QGIS versions with extras
      qgisWithExtras = geospatial.packages.${system}.qgis.override {
        inherit extraPythonPackages;
      };
      qgisLtrWithExtras = geospatial.packages.${system}.qgis-ltr.override {
        inherit extraPythonPackages;
      };
      qgisMasterWithExtras = qgis-upstream.packages.${system}.qgis.override {
        inherit extraPythonPackages;
      };

      pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        # Testing
        pytest
        pytest-cov
        pytest-qt
        mock
        coverage

        # Code quality
        black
        flake8
        isort
        mypy
        pylint
        pep8
        pydocstyle
        bandit

        # Documentation
        mkdocs
        mkdocs-material
        mkdocs-material-extensions
        pymdown-extensions

        # Development
        debugpy
        httpx
        requests
        numpy
        pyyaml

        # Type stubs
        types-requests
        types-pyyaml
      ]);

        # Common QGIS environment variables
        qgisEnv = ''
          export QGIS_CUSTOM_CONFIG_PATH="$HOME/.local/share/QGIS/QGIS3/profiles/${profileName}"
          export QGIS_DEBUG=0
          export QGIS_LOG_FILE="$HOME/${pluginName}.log"

          # Create symlink to plugin if it doesn't exist
          PLUGIN_DIR="$QGIS_CUSTOM_CONFIG_PATH/python/plugins/${pluginName}"
          if [ ! -L "$PLUGIN_DIR" ] && [ ! -d "$PLUGIN_DIR" ]; then
            mkdir -p "$(dirname "$PLUGIN_DIR")"
            ln -s "$PWD/species_explorer" "$PLUGIN_DIR"
            echo "Created symlink: $PLUGIN_DIR -> $PWD/species_explorer"
          fi
        '';

        # Banner for shell
        banner = ''
          echo ""
          echo "  ╔═══════════════════════════════════════════════════════════╗"
          echo "  ║                                                           ║"
          echo "  ║   🦎 Species Explorer - QGIS Plugin Development          ║"
          echo "  ║                                                           ║"
          echo "  ║   Explore biodiversity data from GBIF                     ║"
          echo "  ║                                                           ║"
          echo "  ╚═══════════════════════════════════════════════════════════╝"
          echo ""
          echo "  QGIS Versions:"
          echo "  ───────────────────────────────────────────────────────────────"
          echo "  scripts/start_qgis.sh       Launch QGIS (current release)"
          echo "  scripts/start_qgis_ltr.sh   Launch QGIS LTR"
          echo "  nix run .#qgis-master       Launch QGIS Master (dev)"
          echo ""
          echo "  Development Commands:"
          echo "  ───────────────────────────────────────────────────────────────"
          echo "  nix run .#test          Run tests with coverage"
          echo "  nix run .#format        Format code (black + isort)"
          echo "  nix run .#lint          Lint code (flake8 + pylint)"
          echo "  nix run .#checks        Run pre-commit checks"
          echo "  nix run .#docs-serve    Serve documentation locally"
          echo "  nix run .#docs-build    Build documentation"
          echo "  nix run .#package       Build plugin zip"
          echo "  nix run .#clean         Clean workspace"
          echo "  ───────────────────────────────────────────────────────────────"
          echo ""
          echo "  Made with 💗 by Kartoza | https://kartoza.com"
          echo ""
        '';

    in
    {
      # QGIS packages
      packages.${system} = {
        default = qgisWithExtras;
        qgis = qgisWithExtras;
        qgis-ltr = qgisLtrWithExtras;
        qgis-master = qgisMasterWithExtras;
      };

      # QGIS apps (direct launchers)
      apps.${system} = {
        default = {
          type = "app";
          program = "${qgisWithExtras}/bin/qgis";
        };
        qgis = {
          type = "app";
          program = "${qgisWithExtras}/bin/qgis";
        };
        qgis-ltr = {
          type = "app";
          program = "${qgisLtrWithExtras}/bin/qgis";
        };
        qgis-master = {
          type = "app";
          program = "${qgisMasterWithExtras}/bin/qgis";
        };
        qgis_process = {
          type = "app";
          program = "${qgisWithExtras}/bin/qgis_process";
        };

        # Run tests
        test = {
          type = "app";
          program = toString (pkgs.writeShellScript "test" ''
            echo "Running tests with coverage..."
            ${pythonEnv}/bin/pytest test/ \
              --cov=species_explorer \
              --cov-report=html \
              --cov-report=term \
              -v "$@"
          '');
        };

        # Format code
        format = {
          type = "app";
          program = toString (pkgs.writeShellScript "format" ''
            echo "Formatting code with black and isort..."
            ${pythonEnv}/bin/black species_explorer test scripts
            ${pythonEnv}/bin/isort species_explorer test scripts
            echo "Done!"
          '');
        };

        # Lint code
        lint = {
          type = "app";
          program = toString (pkgs.writeShellScript "lint" ''
            echo "Running flake8..."
            ${pythonEnv}/bin/flake8 species_explorer test
            echo "Running pylint..."
            ${pythonEnv}/bin/pylint species_explorer --rcfile=pylintrc || true
            echo "Done!"
          '');
        };

        # Run pre-commit checks
        checks = {
          type = "app";
          program = toString (pkgs.writeShellScript "checks" ''
            echo "Running pre-commit checks..."
            ${pkgs.pre-commit}/bin/pre-commit run --all-files
          '');
        };

        # Serve documentation
        docs-serve = {
          type = "app";
          program = toString (pkgs.writeShellScript "docs-serve" ''
            echo "Serving documentation at http://localhost:8000"
            ${pythonEnv}/bin/mkdocs serve
          '');
        };

        # Build documentation
        docs-build = {
          type = "app";
          program = toString (pkgs.writeShellScript "docs-build" ''
            echo "Building documentation..."
            ${pythonEnv}/bin/mkdocs build
            echo "Documentation built in site/"
          '');
        };

        # Build plugin package
        package = {
          type = "app";
          program = toString (pkgs.writeShellScript "package" ''
            echo "Building plugin package..."
            ${pkgs.python3}/bin/python3 admin.py build
          '');
        };

        # Clean workspace
        clean = {
          type = "app";
          program = toString (pkgs.writeShellScript "clean" ''
            echo "Cleaning workspace..."
            find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
            find . -type f -name "*.pyc" -delete 2>/dev/null || true
            find . -type f -name "*.pyo" -delete 2>/dev/null || true
            find . -type f -name "core" -delete 2>/dev/null || true
            rm -rf .pytest_cache htmlcov .coverage site build dist 2>/dev/null || true
            echo "Done!"
          '');
        };

        # Security scan
        security = {
          type = "app";
          program = toString (pkgs.writeShellScript "security" ''
            echo "Running bandit security scan..."
            ${pythonEnv}/bin/bandit -r species_explorer -c .bandit.yml
          '');
        };

        # Create symlink to QGIS plugins folder
        symlink = {
          type = "app";
          program = toString (pkgs.writeShellScript "symlink" ''
            ${qgisEnv}
            echo "Plugin symlinked to: $PLUGIN_DIR"
          '');
        };
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          # Python environment
          pythonEnv

          # QGIS (current release in dev shell)
          qgisWithExtras

          # Development tools
          pkgs.pre-commit
          pkgs.git
          pkgs.gnumake
          pkgs.cspell
          pkgs.actionlint
          pkgs.shellcheck
          pkgs.nixfmt-rfc-style
          pkgs.yamllint
          pkgs.gum  # For interactive menus
          pkgs.chafa  # For terminal image display

          # Qt tools
          pkgs.qt5.qttools  # For pyrcc5, pyuic5

          # Archive tools
          pkgs.zip
          pkgs.unzip
        ];

        shellHook = ''
          ${qgisEnv}

          # Create virtual environment for additional packages if needed
          if [ ! -d ".venv" ]; then
            python -m venv .venv
          fi

          # Activate the virtual environment
          source .venv/bin/activate

          # Install any pip requirements
          pip install --upgrade pip > /dev/null
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt > .pip-install.log 2>&1
          fi
          if [ -f requirements-dev.txt ]; then
            pip install -r requirements-dev.txt > .pip-install.log 2>&1
          fi

          # Generate pyrightconfig.json for LSP
          cat > pyrightconfig.json << 'PYRIGHT'
          {
            "include": ["species_explorer", "test"],
            "exclude": [".venv", "build", "dist"],
            "typeCheckingMode": "basic",
            "pythonVersion": "3.9",
            "reportMissingImports": "warning",
            "reportMissingTypeStubs": "none"
          }
PYRIGHT

          # Add PyQt and QGIS to python path for neovim
          export PYTHONPATH="${qgisWithExtras}/share/qgis/python:$PYTHONPATH"

          ${banner}
        '';
      };
    };
}
