import os
import importlib
import toml

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/Documents/WinBar")
        self.validate_config_dir() 

        self.configs = {}
        self.configs["main"] = MainConfig(self.config_dir + "/main.config")

    def validate_config_dir(self):
        if os.path.exists(self.config_dir):
            return
        os.mkdir(self.config_dir)

    def retrieve_components(self, winbar):
        if not self.configs["main"].exists("components"):
            return
        components = self.configs["main"].get("components")
        self.configs["components"] = []
        for component in components:
            component_config = ComponentConfig(component, self.config_dir, self.configs["main"])
            self.configs["components"].append(component_config)
        winbar.register_all_components(self.configs["components"])

    def get(self, name):
        if name in self.configs:
            return self.configs[name]
        raise Exception("config name not found in config manager")

class Config:
    def __init__(self, config_dir: str):
        self.config_dir = config_dir
        self.config_data = {}

    def validate_config_file(self):
        if os.path.exists(self.config_dir):
            return
        raise Exception("config file not found at ", config_dir)

    def exists(self, field):
        return field in self.config_data
    
    def get(self, field):
        if field in self.config_data:
            return self.config_data[field]
        raise Exception("field not found in config")

class MainConfig(Config):
    def __init__(self, config_dir):
        super().__init__(config_dir)
        self.validate_config_file()

    def validate_config_file(self):
        if os.path.exists(self.config_dir):
            self.config_data = toml.load(self.config_dir)
            return
        with open(self.config_dir, 'w') as file:
            self.generate_default_config(file)
    
    def generate_default_config(self, file):
        self.config_data = {
            "winbar": {
                "height": 50,
                "margins": {
                    "left": 5,
                    "right": 5,
                    "top": 5,
                    "bottom": 5
                },
            },
            "colors": {},
            "components": []
        }
        file.write(toml.dumps(self.config_data))
        file.close()

class ComponentConfig(Config):
    def __init__(self, config_data, config_dir, main_configs):
        self.config_data = config_data
        self.config_dir = config_dir
        self.main_configs = main_configs

    def import_component_module(self):
        module_path = self.get_component_module_path()
        spec = importlib.util.spec_from_file_location(self.config_data["name"], module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def get_widget(self):
        module = self.import_component_module()
        return module.get_widget(self.main_configs)

    def get_component_module_path(self):
        return self.config_dir + "/components/" + self.config_data["name"] + ".py"
