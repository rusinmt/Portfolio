## ETL Orchestration Framework

This project encapsulates core concepts of extracting, transforming, and loading data enriched with valuable insights. It aims to automate the process and significantly reduce office worker involvement, making human intervention largely obsolete. The solution is a simplified version of logic prepared for work purposes. It can be hosted on a Linux-based server and scheduled as needed, either triggered when new data flows in or in a timed manner, depending on server traffic and competing tasks.

### Pipeline
<p align="center">
  <img src=https://raw.githubusercontent.com/rusinmt/portfolio/refs/heads/main/Airflow/Images/plan.jpg>
</p>
The workflow extracts raw data and processes it to identify client IDs from images. A fine-tuned YOLOv8 model scans for areas with potential ID numbers. When these areas meet specified conditions, they are processed by a TrOCR pretrained model from Hugging Face. The Python script performs a background check against the database to verify if the returned value matches a valid client number. Upon confirmation, the file is renamed and moved to the renamed tier of the solution architecture.
If no handwriting matches the criteria, the code connects to the Adobe API and proceeds with OCR, which has been selected for its lower hardware requirements. This process handles text-based documents, extracting both the identification number and title using precise logic.
Files that are accurately renamed are then matched via hashlib to their original basenames. These originals are renamed in the raw layer of the architecture. The original scanned documents, now properly renamed, are moved to the enterprise archive for further processing by internal software and ad hoc use.
