Run Command
`.\.venv\Scripts\uvicorn.exe main:app --reload --port 8000`
# PDF API Endpoints

## 1. Render PDF from Template

**Endpoint:**  
`POST /render/pdf`

**Description:**  
Uploads a PDF template and a JSON data payload. The service inserts the data into the template and returns the populated PDF.

**Request Example:**
```bash
curl --location 'http://127.0.0.1:8000/render/pdf' \
  --form 'file=@"/C:/Users/jason/Desktop/IMTG_NoteBook/sample-files/sample pdf files/sample.pdf"' \
  --form 'data="{\"name\": \"Jason\", \"date\": \"2025-07-19\", \"company\": \"OpenAI\"}"'
```

**Form Parameters:**
- `file`  
  - Type: file  
  - Description: PDF template to populate.
- `data`  
  - Type: string (JSON)  
  - Description: JSON object with key/value pairs to insert into the PDF template.  
    - Example keys: `name`, `date`, `company`

**Response:**  
- Returns the rendered PDF binary with the data inserted.

---

## 2. Extract Text from PDF

**Endpoint:**  
`POST /extract/pdf`

**Description:**  
Scans the uploaded PDF for specified keywords and returns any matching strings or locations.

**Request Example:**
```bash
curl --location 'http://127.0.0.1:8000/extract/pdf' \
  --form 'file=@"/C:/Users/jason/Desktop/IMTG_NoteBook/sample-files/sample pdf files/sample.pdf"' \
  --form 'keywords="[\"first name\", \"last name\", \"address\"]"'
```

**Form Parameters:**
- `file`  
  - Type: file  
  - Description: PDF document to scan.
- `keywords`  
  - Type: string (JSON array)  
  - Description: Array of strings to search for within the PDF.  
    - Example: `["first name", "last name", "address"]`

**Response:**  
- Returns a JSON payload with the found occurrences of each keyword (e.g., text snippets or page/position info).
