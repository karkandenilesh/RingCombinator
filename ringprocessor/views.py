import csv
import os
from django.shortcuts import render
from django.conf import settings
from .forms import CSVUploadForm

def transform_csv(input_file):
    combinations = []

    reader = csv.DictReader(input_file.read().decode('utf-8').splitlines())
    
    for row in reader:
        metal_color = row['data__metal_name'].strip()

        shapes = row['data__diamond_can_be_matched_with'].split(',')
        for shape in shapes:
            shape = shape.strip()
            combinations.append(f"Solitaire ring in {metal_color} with {shape}")
    
    return combinations


def upload_csv(request):
    download_link = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            combinations = transform_csv(csv_file)
            filename = save_csv(combinations)
            download_link = f"{settings.MEDIA_URL}{filename}"
    else:
        form = CSVUploadForm()

    return render(request, 'upload.html', {'form': form, 'download_link': download_link})


def save_csv(combinations):
    filename = "output.csv"
    output_path = os.path.join(settings.MEDIA_ROOT, filename)
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Combination'])
        for combination in combinations:
            writer.writerow([combination])

    return filename
