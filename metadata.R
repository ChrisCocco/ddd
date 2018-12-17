metadata = strsplit(as.character(rownames(annotation_tables)), "_") # split filenames
# becomes a list of splited filenames
metadata = setNames(
  do.call(rbind.data.frame, metadata), #transform the list in data.frame
  c("country_year", "region", "sex",
    "context_place", "year", "month", "firstname")
)

metadata$country     = substr(metadata$country_year,1,2)
metadata$year_collect= substr(metadata$country_year,3,4)
metadata$context     = substr(metadata$context_place,1,1)

age_month_numeric = as.numeric(levels(metadata$month))[metadata$month] # it was levels, now xx = NA
age_year_numeric  = as.numeric(levels(metadata$year))[metadata$year]

metadata$rounded_age = ifelse(
  (
    (age_month_numeric >= 0 & age_month_numeric < 6)| is.na(age_month_numeric) # Not like in other projects of GD (X_05 0=>X et X_06 => (X+1))
  ), #!!!!! 7_xx transformed into 7
  age_year_numeric, age_year_numeric+1
)

metadata$age_group = ifelse( 
  metadata$rounded_age <= 9, "young",
  ifelse( 
    metadata$rounded_age <= 12, "middle",
    "old")
)

metadata$age_numeric = ifelse(is.na(age_month_numeric),
                              age_year_numeric, 
                              age_year_numeric + (age_month_numeric/12))


annotation_tables = cbind(annotation_tables, 
                    metadata[,c(
                      "country",
                      "year_collect",
                      "sex",
                      "year",
                      "month",
                      "context",
                      "rounded_age",
                      "age_group",
                      "age_numeric"
                    )]
)