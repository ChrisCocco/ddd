# start 01.06.2017
# useful functions for annotations
# author: Christelle Cocco

#function to retrieve filenames of annotation and annotations themselves
#input: current path and file path where are the annotations 
#output: list, each item of the list = the annotation of one image

#here's a test for collaborative work, let me know it's come out fine!!!
# new test!!!
# yet another test!


get_annotations <- function(path_code, path_annotations){
  setwd(path_annotations)
  file_names = list.files(recursive = T)
  png_files = grep("\\.png", file_names, ignore.case = TRUE)
  if(length(png_files) != 0){
    file_names = file_names[-png_files]
  }
  jpeg_files = grep("\\.jpeg", file_names, ignore.case = TRUE)
  if(length(jpeg_files) != 0){
    file_names = file_names[-jpeg_files]
  }
  jpg_files = grep("\\.jpg", file_names, ignore.case = TRUE)
  if(length(jpg_files) != 0){
    file_names = file_names[-jpg_files]
  }
  
  nb_files = length(file_names)
  
  annotation_tables = list() #set the list of annotations
  
  if (nb_files != 0){
  # Get the annotations files
  
    for (i in 1:length(file_names)){
      annotation_tables[[i]] = read.csv(file_names[i])
      annotation_tables[[i]] = unique(annotation_tables[[i]])
    }
    
    #basename to remove the path to the filename
    names(annotation_tables) = basename(file_names)
    
  }else{
    print("There is no annotated file")
  }
  
  setwd(path_code)
  return(annotation_tables)
}
