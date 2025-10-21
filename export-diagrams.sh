#!/bin/bash

# Script to export all PlantUML diagrams to specified format
# Usage: ./export-diagrams.sh [-png|-svg|-pdf]
# Default: PDF (via SVG conversion)

# Default format
FORMAT="pdf"
USE_SVG_CONVERSION=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -png)
            FORMAT="png"
            shift
            ;;
        -svg)
            FORMAT="svg"
            shift
            ;;
        -pdf)
            FORMAT="pdf"
            shift
            ;;
        -jpeg)
            FORMAT="jpeg"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./export-diagrams.sh [-png|-svg|-pdf|-jpeg]"
            exit 1
            ;;
    esac
done

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/docs/diagrams/src"
OUT_DIR="$SCRIPT_DIR/docs/diagrams/out"
JAR_FILE="$SCRIPT_DIR/plantuml.jar"

# Check if plantuml.jar exists
if [ ! -f "$JAR_FILE" ]; then
    echo "Error: plantuml.jar not found at $JAR_FILE"
    exit 1
fi

# Check if source directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo "Error: Source directory not found at $SRC_DIR"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUT_DIR"

echo "========================================"
echo "Exporting PlantUML Diagrams"
echo "========================================"
echo "Format: $FORMAT"
echo "Source: $SRC_DIR"
echo "Output: $OUT_DIR"
echo "========================================"
echo ""

# Count diagram files
DIAGRAM_COUNT=$(find "$SRC_DIR" -type f \( -name "*.puml" -o -name "*.plantuml" -o -name "*.uml" \) | wc -l | tr -d ' ')

if [ "$DIAGRAM_COUNT" -eq 0 ]; then
    echo "No diagram files found in $SRC_DIR"
    exit 0
fi

echo "Found $DIAGRAM_COUNT diagram file(s)"
echo ""

# Check if PDF conversion tool is available
if [ "$FORMAT" = "pdf" ]; then
    if command -v rsvg-convert &> /dev/null; then
        USE_SVG_CONVERSION=true
        CONVERTER="rsvg-convert"
        echo "Using rsvg-convert for PDF generation"
    elif command -v inkscape &> /dev/null; then
        USE_SVG_CONVERSION=true
        CONVERTER="inkscape"
        echo "Using Inkscape for PDF generation"
    else
        echo "Warning: PDF export requires either 'rsvg-convert' or 'inkscape'"
        echo "Install with: brew install librsvg    (for rsvg-convert)"
        echo "         or: brew install inkscape"
        echo ""
        echo "Attempting direct PDF export (may fail without Apache Batik)..."
        USE_SVG_CONVERSION=false
    fi
    echo ""
fi

# Export diagrams (using source filename)
# PlantUML -o expects relative path from input files
cd "$SRC_DIR" || exit 1

for file in *.puml *.plantuml *.uml; do
    if [ -f "$file" ]; then
        echo "Exporting: $file"
        
        # Get base filename without extension
        basename="${file%.*}"
        
        # If PDF via SVG conversion, export to SVG first
        if [ "$USE_SVG_CONVERSION" = true ]; then
            # Export to SVG first
            java -jar "$JAR_FILE" -tsvg -o "../out" "$file"
            
            # Find the generated SVG file
            latest_svg=$(ls -t "../out/"*.svg 2>/dev/null | head -n 1)
            if [ -n "$latest_svg" ]; then
                target_svg="../out/${basename}.svg"
                # Rename to match source filename
                if [ "$latest_svg" != "$target_svg" ]; then
                    mv "$latest_svg" "$target_svg" 2>/dev/null || true
                fi
                
                # Convert SVG to PDF
                target_pdf="../out/${basename}.pdf"
                if [ "$CONVERTER" = "rsvg-convert" ]; then
                    rsvg-convert -f pdf -o "$target_pdf" "$target_svg"
                elif [ "$CONVERTER" = "inkscape" ]; then
                    inkscape "$target_svg" --export-filename="$target_pdf" --export-type=pdf 2>/dev/null
                fi
                
                # Remove temporary SVG file
                rm "$target_svg" 2>/dev/null || true
                
                echo "  → Generated: ${basename}.pdf"
            fi
        else
            # Direct export to specified format
            java -jar "$JAR_FILE" -t"$FORMAT" -o "../out" "$file"
            
            # Find the generated file and rename it to match source filename
            latest_file=$(ls -t "../out/"*."$FORMAT" 2>/dev/null | head -n 1)
            if [ -n "$latest_file" ]; then
                target_file="../out/${basename}.${FORMAT}"
                # Only rename if it's not already the correct name
                if [ "$latest_file" != "$target_file" ]; then
                    mv "$latest_file" "$target_file" 2>/dev/null || true
                fi
            fi
        fi
    fi
done

cd "$SCRIPT_DIR" || exit 1

# Check if export was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Successfully exported all diagrams!"
    echo "  Format: .$FORMAT"
    echo "  Location: $OUT_DIR"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "✗ Export failed!"
    echo "========================================"
    exit 1
fi

