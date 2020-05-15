library(readxl)

xlsx <- "E:/2020W20 Input.xlsx"
decoder <- read_excel(xlsx, sheet = "Cipher") 
cipher_text <- read_excel(xlsx, sheet = "Encrypted Message")['Encrypted Message'][[1]]

plain_text <- chartr(paste(decoder[,2]), paste(decoder[,1]), cipher_text)
plain_text