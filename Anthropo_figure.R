# 24.11.2016, 01.12.2016
# new start 16.06.2017

WD <- tryCatch(dirname(rstudioapi::getSourceEditorContext()$path), error=function(e){return(NULL)}) # for Rstudio
if (!is.null(WD)){
  setwd(WD)
}else{ 
  (WD <- getwd()) # source and Rscript
  if (!is.null(WD)) setwd(WD)
}
source("utils_position.R")


path_code = WD

path_annot = "../DATA/ANNOTATION_ANT"
if (! dir.exists(path_annot)) stop(paste(path_annot, "does not exist! please verify!"))

annotation_tables = get_annotations(path_code, path_annot)


nb_annot = length(annotation_tables)

file_names = names(annotation_tables)


# Remove name of annotator, word "annotation", size of the image, etc. to keep just
# the filename
filenames = substr(file_names, 12, (regexpr("-r", file_names, perl = F) - 1)) #file_names = names(annotation_tables) #if done with utils



properties = c("heads","eyes","noses", "mouths", "ears", "hair", "beard", 
               "clothes", "arms", "hands", "legs", "feet", "accessories", 
               "celestial", "elemental", "archi", "vegetation", "Box_type")

# creation of the empty data.frame of integers to store the results
anthropo_fig = data.frame(matrix(integer(), length(filenames), 
                                 length(properties),
                             #row and column names
                             dimnames=list(filenames, properties)), 
                      stringsAsFactors=F
)

i = 6

if(sum(annotation_tables[[i]]$Feature.code == "R1") >= 1){
  
  box_x1 = annotation_tables[[i]]$x1.onFile[
    grepl("C", annotation_tables[[i]]$Feature.code)]

  box_x2 = annotation_tables[[i]]$x2.onFile[
    grepl("C", annotation_tables[[i]]$Feature.code)]
  
  box_y1 = annotation_tables[[i]]$y1.onFile[
    grepl("C", annotation_tables[[i]]$Feature.code)]
  box_y2 = annotation_tables[[i]]$y2.onFile[
    grepl("C", annotation_tables[[i]]$Feature.code)]
  
  # print(box_x1)
  # print(box_x2)
  # print(box_y1)
  # print(box_y2)
  
  god_x = annotation_tables[[i]]$x1.onFile[
    annotation_tables[[i]]$Feature.code=="R1"] 
  god_y = annotation_tables[[i]]$y1.onFile[
    annotation_tables[[i]]$Feature.code=="R1"] 
  if(length(box_x1) != 0 ){ #doesn't try if box_x1 is empty 
    # TO BE CONTINUED (See Center_mass_Gods.R)
    god_with_box = c()
    
    for (k in 1:length(box_x1)){
      
      for (l in 1:length(god_x)){
        
        if (god_x[l] > box_x1[k] && god_x[l] < box_x2[k] && 
            god_y[l] > box_y1[k] && god_y[l] < box_y2[k]){
          god_with_box = c(god_with_box, c(god_x[l], god_y[l], box_x1[k], 
                                           box_y1[k], box_x2[k], box_y2[k])) #TO BE TESTED, Then add if god_with_box == 6, else print(more than one god in box)
          
        } else{
          print(cat("there is", length(god_x), "god(s) in file: ", filenames[i],
                    "but it/they is/are not in THIS box")) #TO BE CHANGED, happens also when there are empty box, even if one god is in box (i= 6 dans sample)
        }
      }#end for
    }#end for
    
  }else{
    # TO BE TESTED
    print(cat("there is", length(god_x), "god(s) in file: ", filenames[i],
              "but it/they is/are not in a box"))
  }
} else{
  print(cat("there is no god in file: ", filenames[i]))
}