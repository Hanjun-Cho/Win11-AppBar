import importlib
import os
import shutil
from configs.components_config import ComponentsFields 

class ComponentManager():
    def __init__(self, config_dir, components_config):
        self.components_dir = config_dir + "/Components"
        self.components_config = components_config
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(self.components_dir):
            os.mkdir(self.components_dir)

            # copies default components into components folder
            default_components_dir = self.current_dir + "/default/Components"
            shutil.copytree(default_components_dir, self.components_dir, dirs_exist_ok=True)

    def init_components(self, layout_config):
        layout = {}
        
        left_components = self.components_config[ComponentsFields.LEFT]
        left_modules = self.init_component_list(left_components, layout_config)

        center_components = self.components_config[ComponentsFields.CENTER]
        center_modules = self.init_component_list(center_components, layout_config)

        right_components = self.components_config[ComponentsFields.RIGHT]
        right_modules = self.init_component_list(right_components, layout_config)

        layout = {
            ComponentsFields.LEFT: left_modules,
            ComponentsFields.CENTER: center_modules,
            ComponentsFields.RIGHT: right_modules
        }

        self.component_layout = layout 
        return layout

    def init_component_list(self, component_list, layout_config):
        components = []
        for component_name in component_list:
            component_file_name = component_name + ".py"
            component_dir = self.components_dir + "/" + component_file_name

            if not os.path.exists(component_dir):
                print(component_file_name + " does not exist in component files")

            module = self.import_component_module(component_name, component_dir)
            components.append(module.get_widget(layout_config))
        return components

    def import_component_module(self, component_name, component_dir):
        spec = importlib.util.spec_from_file_location(component_name, component_dir)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def get_component_layout(self):
        return self.component_layout
