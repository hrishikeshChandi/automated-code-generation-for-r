options(repos = c(CRAN = "https://cloud.r-project.org"))

required_packages <- c("lintr", "pryr")
new_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(new_packages)) install.packages(new_packages)

library(lintr)
library(pryr)

format_bytes <- function(bytes) {
  units <- c("B", "KB", "MB", "GB", "TB")
  i <- 1L
  while (bytes >= 1024 && i < length(units)) {
    bytes <- bytes / 1024
    i <- i + 1L
  }
  sprintf("%.2f %s", bytes, units[i])
}

code_file <- "trial.R"
report_file <- "analysis_report.txt"

analysis_output <- character()
append_output <- function(...) {
  line <- paste0(..., collapse = "")
  analysis_output <<- c(analysis_output, line)
}

append_output("==== Automated Code Analysis Report ====\n")

append_output("\n1. Code Quality (Lint):\n")
lint_results <- lint(code_file)
if (length(lint_results) == 0) {
  append_output("- No linting issues found.\n")
} else {
  lint_text <- capture.output(print(lint_results))
  append_output(paste0(lint_text, collapse = "\n"), "\n")
}

append_output("\n2. Code Execution:\n")
warnings_list <- character()
success <- TRUE
start_time <- Sys.time()
mem_before <- mem_used()

execution_output <- capture.output({
  tryCatch({
    source(code_file, echo = TRUE, max.deparse.length = 1000)
  }, warning = function(w) {
    warnings_list <<- c(warnings_list, conditionMessage(w))
    invokeRestart("muffleWarning")
  }, error = function(e) {
    append_output("ERROR during execution: ", e$message, "\n")
    success <<- FALSE
  })
})

mem_after <- mem_used()
end_time <- Sys.time()
mem_diff <- mem_after - mem_before

append_output(execution_output, "\n")

append_output("\n3. Performance Metrics:\n")
append_output(sprintf("Execution time: %.2f seconds\n", as.numeric(difftime(end_time, start_time, units = "secs"))))
append_output(sprintf("Memory used: %s\n", format_bytes(mem_diff)))

append_output("\n4. Warnings:\n")
if (length(warnings_list) > 0) {
  for (w in warnings_list) {
    append_output("- ", w, "\n")
  }
} else {
  append_output("- None\n")
}

append_output("\n5. Summary:\n")
if (length(lint_results) == 0) {
  append_output("- ✅ Code style is clean.\n")
} else {
  append_output("- ⚠️ Linting issues found. Please review.\n")
}
if (success) {
  append_output("- ✅ Code executed successfully.\n")
} else {
  append_output("- ❌ Code execution failed.\n")
}

writeLines(analysis_output, con = report_file)
