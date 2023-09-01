# -*- coding: utf-8 -*-

import os

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc


def get_Rhino_file(_dir):

    path_list = []
    
    for root, dirs, files in os.walk(_dir, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            path = str(path)

            if path.endswith(".3dm"):
                path_list.append(path)

    return path_list


def get_GH_file(_dir):

    path_list = []

    for root, dirs, files in os.walk(_dir, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            path = str(path)

            if path.endswith(".gh"):
                path_list.append(path)

    return path_list


def read_recipe(file_path):
    
    recipes = []
    
    with open(file_path) as f:
        all_ = f.read()
        elms = all_.split('\n')
        
        for elm in elms:
            # print(elm)
            if elm.endswith(".gh"):
                recipes.append(elm)

    return recipes


def run_GH(gh_file):

    gh.LoadEditor()
    gh.CloseAllDocuments()
    gh.ShowEditor()
    
    gh.OpenDocument(gh_file)
    
    gh.AssignDataToParameter("RhinoPython_bake", True)
    
    gh.RunSolver(True)


def loop_GH(gh_files, recipes):

    ### (2) Multi run
    for recipe in recipes:

        for gh_file in gh_files:
            
            if recipe in gh_file:
                run_GH(gh_file)
            
    gh.CloseAllDocuments()
    gh.HideEditor()


def open_close(Rhino_file, GH_files, recipes):

    rhino_file = '"' + Rhino_file + '"'
    
    rs.Command('_-Open {}'.format(rhino_file))

    loop_GH(GH_files, recipes)

    rs.Command("_Save")





gh = Rhino.RhinoApp.GetPlugInObject("Grasshopper")

sc.doc = Rhino.RhinoDoc.ActiveDoc

### Init
rs.Command("-New \"Large Objects - Millimeters.3dm\"")



rhino_folder = rs.BrowseForFolder(message="select_Rhino_Folder")
rhino_files = get_Rhino_file(rhino_folder)

print("Rhino Folder : {}".format(os.path.basename(rhino_folder)))


gh_foloder = rs.BrowseForFolder(message="Select_GH_Folder")
gh_files = get_GH_file(gh_foloder)


recipe_path = rs.OpenFileName(title="Select_Recipe")
recipes = read_recipe(recipe_path)

print("Recipe Name : {}".format(os.path.basename(recipe_path)))




### (1) Check, gh all exist
for recipe in recipes:
    
    exit_flag = False
    
    for ghfile in gh_files:
        if recipe in ghfile:
            # print(ghfile)
            exit_flag = True
    
    if exit_flag == False:
        print("Error : {} does not exit gh_folder".format(recipe))
        exit()



for rhino_file in rhino_files:
    open_close(rhino_file, gh_files, recipes)
