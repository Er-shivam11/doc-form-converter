
```markdown
# Excel to Table Django Application

A Django-based web application that allows users to upload Word (`.docx`) and Excel files, extract table and worksheet data, manage templates, and control user permissions. This project is designed to streamline document-to-database workflows and form processing with template mapping and user-level access control.

---

## Features

- **User Authentication**
  - Login for superusers and normal users.
  - Redirect users based on role.

- **Template Management**
  - Upload Word (`.docx`) templates.
  - Extract headers and table data automatically.
  - Save template metadata to the database.

- **Form Uploading**
  - Upload forms associated with specific templates.
  - Map form fields with templates.

- **Data Processing**
  - Parse uploaded templates using `python-docx`.
  - Extract and standardize table rows.
  - Save parsed data to database for further processing.

- **User Permissions**
  - Assign forms and templates to users.
  - Control access to forms using permission settings.

- **Form Display & Updates**
  - Display parsed form data in tabular format.
  - Allow updates to standard values through the interface.

- **Dockerized Setup**
  - Full-stack application with MySQL and phpMyAdmin.
  - Docker Compose configuration for easy deployment.

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** MySQL
- **Frontend:** HTML templates
- **Libraries:** 
  - `pandas` for data processing
  - `python-docx` for Word document parsing
  - `pdfplumber` for PDF support (if needed)
- **Docker:** For containerized deployment

---

## Project Structure

```

<img width="372" height="569" alt="image" src="https://github.com/user-attachments/assets/691277e1-948d-4a4d-a1b2-1bba490bd1e1" />


````

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo_url>
cd excel_to_table
````

### 2. Docker Setup

Make sure you have Docker and Docker Compose installed. The `docker-compose.yml` defines three services:

1. **MySQL Database**

   * Port: `33066`
   * Database: `etot`
   * Username: `root`
   * Password: `root`
2. **phpMyAdmin**

   * Port: `9090`
3. **Django Application**

   * Port: `8000`
   * Depends on the MySQL service

Start the services:

```bash
docker-compose up --build
```

### 3. Django Migrations

If running inside the Docker container:

```bash
docker-compose exec excel_to_table python manage.py makemigrations
docker-compose exec excel_to_table python manage.py migrate
```

### 4. Create Superuser

```bash
docker-compose exec excel_to_table python manage.py createsuperuser
```

### 5. Access the Application

* **Django App:** `http://localhost:8000`
* **phpMyAdmin:** `http://localhost:9090`

  * Server: `db`
  * User: `root`
  * Password: `root`

---

## Usage

1. **Login**

   * Use superuser credentials or assigned user credentials.

2. **Upload Template**

   * Navigate to "Add Template".
   * Upload `.docx` template files.
   * System parses headers and tables and stores data.

3. **Select Template & Assign Permissions**

   * Assign templates to specific users with expiry dates.

4. **Upload Forms**

   * Upload forms using the associated template.

5. **Edit and Update Form Data**

   * View parsed form data.
   * Update standard values as required.

6. **View User-Assigned Forms**

   * Users can access forms assigned to them based on permissions.

---

## Dependencies

* Django
* pandas
* python-docx
* pdfplumber
* bootstrap-datepicker-plus (for date picker widgets)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Notes

* Ensure uploaded templates are properly formatted `.docx` files.
* The application currently supports MySQL; adjust settings if using another database.
* All sensitive credentials (like API keys or database passwords) should be handled via environment variables.

---

## License

This project is licensed under the MIT License.


