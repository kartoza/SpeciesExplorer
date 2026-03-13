-- SpeciesExplorer - Neovim project configuration
-- This file provides project-specific keybindings and settings
-- All project commands are under <leader>p (project prefix)

local ok, wk = pcall(require, "which-key")
if not ok then
  vim.notify("which-key not found, skipping project keybindings", vim.log.levels.WARN)
  return
end

-- Helper function to run commands in terminal
local function run_in_terminal(cmd, opts)
  opts = opts or {}
  local term_opts = {
    direction = opts.direction or "horizontal",
    close_on_exit = opts.close_on_exit or false,
  }

  -- Try to use toggleterm if available
  local has_toggleterm, toggleterm = pcall(require, "toggleterm")
  if has_toggleterm then
    local Terminal = require("toggleterm.terminal").Terminal
    local term = Terminal:new({
      cmd = cmd,
      direction = term_opts.direction,
      close_on_exit = term_opts.close_on_exit,
      on_open = function(t)
        vim.cmd("startinsert!")
      end,
    })
    term:toggle()
  else
    -- Fallback to built-in terminal
    vim.cmd("split | terminal " .. cmd)
    vim.cmd("startinsert")
  end
end

-- Project-specific keybindings
wk.add({
  -- Main project prefix
  { "<leader>p", group = "Project (SpeciesExplorer)" },

  -- QGIS commands
  { "<leader>pq", group = "QGIS" },
  {
    "<leader>pqq",
    function()
      run_in_terminal("nix run .#qgis")
    end,
    desc = "Launch QGIS",
  },
  {
    "<leader>pqs",
    function()
      run_in_terminal("./scripts/start_qgis.sh")
    end,
    desc = "Launch QGIS (interactive)",
  },
  {
    "<leader>pql",
    function()
      run_in_terminal("nix run .#symlink")
    end,
    desc = "Symlink plugin to QGIS",
  },

  -- Testing commands
  { "<leader>pt", group = "Testing" },
  {
    "<leader>ptt",
    function()
      run_in_terminal("nix run .#test")
    end,
    desc = "Run all tests",
  },
  {
    "<leader>ptf",
    function()
      local file = vim.fn.expand("%:p")
      run_in_terminal("nix run .#test -- " .. file)
    end,
    desc = "Test current file",
  },
  {
    "<leader>ptl",
    function()
      run_in_terminal("nix run .#test -- --lf")
    end,
    desc = "Run last failed tests",
  },
  {
    "<leader>ptv",
    function()
      run_in_terminal("nix run .#test -- -v")
    end,
    desc = "Run tests verbose",
  },
  {
    "<leader>ptc",
    function()
      vim.cmd("!open htmlcov/index.html 2>/dev/null || xdg-open htmlcov/index.html 2>/dev/null")
    end,
    desc = "Open coverage report",
  },

  -- Code quality commands
  { "<leader>pc", group = "Code Quality" },
  {
    "<leader>pcf",
    function()
      run_in_terminal("nix run .#format")
    end,
    desc = "Format code (black + isort)",
  },
  {
    "<leader>pcl",
    function()
      run_in_terminal("nix run .#lint")
    end,
    desc = "Lint code (flake8 + pylint)",
  },
  {
    "<leader>pcb",
    function()
      local file = vim.fn.expand("%:p")
      run_in_terminal("black " .. file)
    end,
    desc = "Black format current file",
  },
  {
    "<leader>pci",
    function()
      local file = vim.fn.expand("%:p")
      run_in_terminal("isort " .. file)
    end,
    desc = "isort current file",
  },
  {
    "<leader>pcs",
    function()
      run_in_terminal("nix run .#security")
    end,
    desc = "Security scan (bandit)",
  },

  -- Documentation commands
  { "<leader>pd", group = "Documentation" },
  {
    "<leader>pds",
    function()
      run_in_terminal("nix run .#docs-serve")
    end,
    desc = "Serve docs locally",
  },
  {
    "<leader>pdb",
    function()
      run_in_terminal("nix run .#docs-build")
    end,
    desc = "Build documentation",
  },
  {
    "<leader>pdo",
    function()
      vim.cmd("!open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null")
    end,
    desc = "Open docs in browser",
  },

  -- Packaging commands
  { "<leader>pp", group = "Packaging" },
  {
    "<leader>ppz",
    function()
      run_in_terminal("nix run .#package")
    end,
    desc = "Build plugin zip",
  },
  {
    "<leader>pps",
    function()
      run_in_terminal("nix run .#symlink")
    end,
    desc = "Symlink to QGIS plugins",
  },

  -- Utility commands
  { "<leader>pu", group = "Utilities" },
  {
    "<leader>puc",
    function()
      run_in_terminal("nix run .#clean")
    end,
    desc = "Clean workspace",
  },
  {
    "<leader>pup",
    function()
      run_in_terminal("nix run .#checks")
    end,
    desc = "Run pre-commit checks",
  },
  {
    "<leader>pun",
    function()
      run_in_terminal("nix develop")
    end,
    desc = "Enter nix develop shell",
  },
  {
    "<leader>pur",
    function()
      run_in_terminal("pyrcc5 -o species_explorer/resources.py species_explorer/resources.qrc")
    end,
    desc = "Compile resources",
  },

  -- Git commands
  { "<leader>pg", group = "Git" },
  {
    "<leader>pgs",
    function()
      run_in_terminal("git status")
    end,
    desc = "Git status",
  },
  {
    "<leader>pgd",
    function()
      run_in_terminal("git diff")
    end,
    desc = "Git diff",
  },
  {
    "<leader>pgl",
    function()
      run_in_terminal("git log --oneline -20")
    end,
    desc = "Git log (last 20)",
  },
  {
    "<leader>pgp",
    function()
      run_in_terminal("git pull")
    end,
    desc = "Git pull",
  },
})

-- LSP configuration for this project
local lspconfig_ok, lspconfig = pcall(require, "lspconfig")
if lspconfig_ok then
  -- Configure pyright for this project
  local util = require("lspconfig.util")

  -- Find QGIS Python paths
  local qgis_paths = {
    "/usr/share/qgis/python",
    "/usr/share/qgis/python/plugins",
    "/usr/lib/python3/dist-packages",
  }

  -- Add nix store paths if available
  local nix_qgis = vim.fn.system("which qgis 2>/dev/null"):gsub("%s+", "")
  if nix_qgis ~= "" then
    local nix_path = nix_qgis:match("(.*/nix/store/[^/]+)")
    if nix_path then
      table.insert(qgis_paths, nix_path .. "/share/qgis/python")
      table.insert(qgis_paths, nix_path .. "/share/qgis/python/plugins")
    end
  end

  -- Create pyrightconfig.json if it doesn't exist
  local project_root = vim.fn.getcwd()
  local pyrightconfig_path = project_root .. "/pyrightconfig.json"

  if vim.fn.filereadable(pyrightconfig_path) == 0 then
    local config = {
      include = { "species_explorer", "test" },
      exclude = { ".venv", "build", "dist", "__pycache__" },
      typeCheckingMode = "basic",
      pythonVersion = "3.9",
      extraPaths = qgis_paths,
      reportMissingImports = "warning",
      reportMissingTypeStubs = "none",
    }

    local file = io.open(pyrightconfig_path, "w")
    if file then
      file:write(vim.fn.json_encode(config))
      file:close()
    end
  end
end

-- DAP (Debug Adapter Protocol) configuration
local dap_ok, dap = pcall(require, "dap")
if dap_ok then
  -- Python debugger configuration
  dap.adapters.python = {
    type = "executable",
    command = "python",
    args = { "-m", "debugpy.adapter" },
  }

  dap.configurations.python = dap.configurations.python or {}

  -- Add QGIS debugging configuration
  table.insert(dap.configurations.python, {
    type = "python",
    request = "attach",
    name = "Attach to QGIS",
    connect = {
      host = "127.0.0.1",
      port = 5678,
    },
    pathMappings = {
      {
        localRoot = vim.fn.getcwd() .. "/species_explorer",
        remoteRoot = vim.fn.expand("~")
          .. "/.local/share/QGIS/QGIS3/profiles/SpeciesExplorer/python/plugins/SpeciesExplorer",
      },
    },
  })

  -- Add project-specific debug keybindings
  wk.add({
    { "<leader>px", group = "Debug" },
    {
      "<leader>pxb",
      function()
        dap.toggle_breakpoint()
      end,
      desc = "Toggle breakpoint",
    },
    {
      "<leader>pxc",
      function()
        dap.continue()
      end,
      desc = "Continue",
    },
    {
      "<leader>pxs",
      function()
        dap.step_over()
      end,
      desc = "Step over",
    },
    {
      "<leader>pxi",
      function()
        dap.step_into()
      end,
      desc = "Step into",
    },
    {
      "<leader>pxo",
      function()
        dap.step_out()
      end,
      desc = "Step out",
    },
    {
      "<leader>pxa",
      function()
        dap.continue()
      end,
      desc = "Attach to QGIS",
    },
    {
      "<leader>pxr",
      function()
        dap.repl.open()
      end,
      desc = "Open REPL",
    },
  })
end

-- Project-specific settings
vim.opt_local.tabstop = 4
vim.opt_local.shiftwidth = 4
vim.opt_local.expandtab = true
vim.opt_local.colorcolumn = "120"

-- Notification that config loaded
vim.notify("SpeciesExplorer project configuration loaded", vim.log.levels.INFO)
