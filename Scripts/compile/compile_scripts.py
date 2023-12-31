import os
from Utilities.unpyc3_compiler import Unpyc3PythonCompiler

release_dir = os.path.join('..', '..', 'Release')

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join(release_dir, 'BBSurvival'),
    names_of_modules_include=('bbsurvival', 'requirecookingingredients', 'nomorequickmeals', 'lightonfire', 'lightonfire_ignorefire'),
    output_ts4script_name='bbsurvival'
)

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join(release_dir, 'NoMoreQuickMeals'),
    names_of_modules_include=('nomorequickmeals',),
    output_ts4script_name='nomorequickmeals'
)

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join(release_dir, 'RequireCookingIngredients'),
    names_of_modules_include=('requirecookingingredients',),
    output_ts4script_name='requirecookingingredients'
)

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join(release_dir, 'LightOnFire'),
    names_of_modules_include=('lightonfire',),
    output_ts4script_name='lightonfire'
)

Unpyc3PythonCompiler.compile_mod(
    folder_path_to_output_ts4script_to=os.path.join(release_dir, 'LightOnFire'),
    names_of_modules_include=('lightonfire_ignorefire',),
    output_ts4script_name='lightonfire_ignorefire'
)
