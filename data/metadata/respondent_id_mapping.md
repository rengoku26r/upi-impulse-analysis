# Respondent ID Mapping Documentation

## Purpose

This document defines the structure used to generate unique respondent IDs for the **UPI Impulse Trap Analysis** project.

The goal is to:

- Maintain respondent anonymity
- Preserve dataset source (college-level information)
- Enable consistent tracking across merged datasets

---

## College Mapping

Each dataset source (college/group) is assigned a numeric identifier:

| College / Source  | Code |
|-------------------|------|
| aiims_jodhpur     | 1    |
| jaipur_colleges   | 2    |
| iit_bhilai        | 3    |
| iit_delhi         | 4    |

---

## ID Structure

Each respondent ID follows the format:
{college_code}{row_number}

- `college_code` → numeric identifier for the dataset source  
- `row_number` → original row number within that dataset  

---

## Example

1021

Interpretation:

- `1` → aiims_jodhpur  
- `021` → 21st response in that dataset  

---

## Notes

- Respondent IDs are **unique across all datasets**
- IDs are generated **before merging datasets**
- Email and other personally identifiable information (PII) are **removed from analysis dataset**
- IDs are used for:
  - Dataset merging
  - Record tracking
  - Analysis consistency

---

## Data Privacy

- Email addresses (if collected) are stored separately and are **not included** in the analysis dataset
- This ensures compliance with **basic data privacy practices**
- The analysis dataset is fully **anonymized**
