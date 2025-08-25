# ------------------------------
# Step 0: Base Image
# ------------------------------
FROM python:3.13.3-slim

# ------------------------------
# Step 1: Install system dependencies
# ------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gfortran \
    libatlas-base-dev \
    python3-dev \
    libffi-dev \
    libssl-dev \
    git \
 && rm -rf /var/lib/apt/lists/*


# ------------------------------
# Step 2: Set working directory
# ------------------------------
WORKDIR /botapp

# ------------------------------
# Step 3: Copy only requirements first
# ------------------------------
COPY requirements.txt .

# ------------------------------
# Step 4: Install Python dependencies
# ------------------------------
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ------------------------------
# Step 5: Copy the rest of your code
# ------------------------------
COPY . .

# ------------------------------
# Step 6: Run the bot
# ------------------------------
CMD ["python", "main.py"]