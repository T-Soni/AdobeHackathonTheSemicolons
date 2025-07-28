# Adobe Hackathon - Round 1A Solution

🧠 **Overview**
This project extracts a structured document outline—including the Title and Headings (H1, H2, H3)—from PDF files. For each PDF placed in the `/app/input` directory, the solution generates a corresponding JSON file in the `/app/output` directory.

---

### ✨ **How It Works**
The solution uses the **PyMuPDF** library to parse PDF content block by block. It identifies structural elements like headings by applying a set of heuristics to text properties:

* **Font Size:** Larger than the document's baseline paragraph font.
* **Font Weight:** Bolded text.
* **Casing:** ALL CAPS text.
* **Line Length:** Shorter than typical paragraph lines.
* **Alignment:** Centered text is often a title or major heading.

---

### 📦 **Dependencies**
All dependencies are installed and managed inside the Docker container for a consistent and isolated runtime environment.
* Python 3.9
* PyMuPDF

---

### 🚀 **Build & Run Instructions**

**Prerequisites:** You must have **Docker** installed on your system.

#### **1. Clone the Repository**
First, clone this repository to your local machine.

```bash
git clone <your-repo-url>
cd <repository-folder>
```
#### **2. Build the Docker Image**
Build the Docker image using the provided Dockerfile. You can replace my-solution with any name you prefer.

```bash
docker build --platform linux/amd64 -t my-solution .
```
#### **2. Build the Docker Image**
Build the Docker image using the provided Dockerfile. You can replace my-solution with any name you prefer.

```bash
docker build --platform linux/amd64 -t my-solution .
```
#### **3. Prepare Input Files**
Create input and output directories in the project root.

```bash
mkdir input output
```
Place one or more .pdf files that you want to process into the newly created input/ folder.

#### **4. Run the Solution**
Execute the following command to run the container. It mounts your local folders, runs the script, and ensures no network access is used, as per the hackathon rules.

For Linux & macOS:
```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  --network none \
  my-solution
```
For Windows (PowerShell):
```bash
docker run --rm `
  -v "${PWD}/input:/app/input" `
  -v "${PWD}/output:/app/output" `
  --network none `
  my-solution
```

#### **📄 Output Format**
fter the script runs, the output/ directory will contain a .json file for each input PDF. The structure of the JSON is as follows:
```JSON

{
  "title": "The Main Title of the Document",
  "outline": [
    {
      "level": "H1",
      "text": "First Major Heading",
      "page": 1
    },
    {
      "level": "H2",
      "text": "A Subsection Heading",
      "page": 2
    },
    {
      "level": "H3",
      "text": "A More Granular Sub-point",
      "page": 2
    }
  ]
}
```

#### **✅ Hackathon Constraints Compliance**
* Offline Execution: Runs completely offline (--network none).

* CPU Only: Operates entirely on CPU (--platform linux/amd64).

* Model Size: Uses no pre-trained models, so the size constraint is met.

* Performance: Processes a 50-page PDF in well under 10 seconds.

* Containerization: Fully containerized using the provided Dockerfile.
