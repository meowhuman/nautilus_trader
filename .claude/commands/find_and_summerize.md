# Find and Summarize Files

> Recursively find all files in the codebase with the given **SEARCH_DIRECTORY** and **FILE_FILTERING** argument hints, then summarize them in the log directory.

## Purpose

Find and summarize specific files in the codebase and save the summary to a log directory.

## Variables

```
SEARCH_DIRECTORY = '' [red-name]
FILE_FILTERING = 'any' or 'specific' [red-name]
```

## Instructions

### 1. Search
- Recursively find all files in the `SEARCH_DIRECTORY` with the given `FILE_FILTERING` with the aim of understanding its purpose and functionality.
- Read and analyze each file in the codebase. Ensure it's purpose and functionality.
- Continue your search until you have summarized every file in the `SEARCH_DIRECTORY` that matches the `FILE_FILTERING`.

### 2. Report
- IMPORTANT: Create the sentence summaries for each file.
- In the first sentence, describe the file's purpose and functionality.
- In the second sentence (if needed), describe any data structures, key functions, or dependencies.

### 3. Workflow
1. Find all files in the `SEARCH_DIRECTORY` with the given `FILE_FILTERING` with the aim of understanding its purpose and functionality.
2. Read as much code as you need to understand it's purpose and full functionality.
3. Continue your search until you have summarized every file in the `SEARCH_DIRECTORY` that matches the `FILE_FILTERING`.
4. Return the summary in the correct `REPORT_FORMAT` format.
