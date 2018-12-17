# Execute retrieve_filenmaes.R first
# 09.11.2016 - 17.11.2016


# For one sheet, count the number of element types annotated 

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

annotations = get_annotations(path_code, path_annot)


nb_annot = length(annotations)

filenames = names(annotations)

file_names = filenames
annotation_tables = annotations

# Remove name of annotator, word "annotation", size of the image, etc. to keep just
# the filename
filenames = substr(file_names, 12, (regexpr("-r", file_names, perl = F) - 1)) #file_names = names(annotation_tables) #if done with utils


properties = c("heads","eyes","noses", "mouths", "ears", "hair", "beard", "clothes", "arms",
               "hands", "legs", "feet")#, "accessories", "celestial", "elemental", "archi",
#               "vegetation", "human", "non_human", "text", "blank", "other_char")

# creation of the empty data.frame of integers to store the results
anthropo = data.frame(matrix(integer(), length(filenames), length(properties),
                       dimnames=list(filenames, properties)), #row and column names
                stringsAsFactors=F
)

for (i in 1:length(filenames)){
  anthropo$heads[i]  = sum(annotation_tables[[i]]$Feature.code == "A1.2.1")
  anthropo$eyes[i]   = sum(grepl("A1.2.2", annotation_tables[[i]]$Feature.code))
  anthropo$noses[i]  = sum(annotation_tables[[i]]$Feature.code == "A1.2.3")
  anthropo$mouths[i] = sum(grepl("A1.2.4", annotation_tables[[i]]$Feature.code))
  anthropo$ears[i]   = sum(grepl("A1.2.5", annotation_tables[[i]]$Feature.code))
  
  # "chauve" = 1.2.6.3 enlevé, mais à vérifier, car pas dans mon échantillon
  anthropo$hair[i]   = sum(grepl("A1.2.6", annotation_tables[[i]]$Feature.code)) - 
    sum(annotation_tables[[i]]$Feature.code == "A1.2.6.3")
  anthropo$beard[i]  = sum(annotation_tables[[i]]$Feature.code == "A1.2.7")
  anthropo$clothes[i]= sum(grepl("A1.3", annotation_tables[[i]]$Feature.code))
  anthropo$arms[i]   = sum(annotation_tables[[i]]$Feature.code == "A1.4")
  anthropo$hands[i]  = sum(grepl("A1.5", annotation_tables[[i]]$Feature.code))
  anthropo$legs[i]   = sum(annotation_tables[[i]]$Feature.code == "A1.6")
  anthropo$feet[i]   = sum(grepl("A1.7", annotation_tables[[i]]$Feature.code))
  
  # anthropo$accessories[i]= sum(grepl("A2", annotation_tables[[i]]$Feature.code))
  # anthropo$celestial[i]  = sum(grepl("A3", annotation_tables[[i]]$Feature.code))
  # anthropo$elemental[i]  = sum(grepl("A4", annotation_tables[[i]]$Feature.code))
  # anthropo$archi[i]      = sum(grepl("A5", annotation_tables[[i]]$Feature.code))
  # anthropo$vegetation[i] = sum(grepl("A6", annotation_tables[[i]]$Feature.code))
  
  # anthropo$human[i]      = sum(annotation_tables[[i]]$Feature.code == "C1")
  # anthropo$non_human[i]  = sum(annotation_tables[[i]]$Feature.code == "C2")
  # anthropo$text[i]       = sum(annotation_tables[[i]]$Feature.code == "C3")
  # anthropo$blank[i]      = sum(annotation_tables[[i]]$Feature.code == "C4")
  # anthropo$other_char[i] = sum(annotation_tables[[i]]$Feature.code == "C5")
}



write.csv(anthropo, file = "features/anthropo.csv")
