#!/bin/bash
# Create deployment package for Vision PDF QA System
# Run this to package the deployment folder for easy transfer

echo "=================================================="
echo "  Creating Vision PDF QA Deployment Package"
echo "=================================================="
echo

# Check if deployment folder exists
if [ ! -d "vision_qa_deployment" ]; then
    echo "❌ Error: vision_qa_deployment folder not found"
    exit 1
fi

# Create timestamp for versioning
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
PACKAGE_NAME="vision_qa_deployment_${TIMESTAMP}.tar.gz"

echo "📦 Packaging files..."
tar -czf "$PACKAGE_NAME" vision_qa_deployment/

if [ $? -eq 0 ]; then
    echo "✅ Package created successfully!"
    echo
    echo "File: $PACKAGE_NAME"
    echo "Size: $(du -h "$PACKAGE_NAME" | cut -f1)"
    echo
    echo "=================================================="
    echo "  Transfer Instructions"
    echo "=================================================="
    echo
    echo "To deploy to remote systems:"
    echo
    echo "1. Transfer the package:"
    echo "   scp $PACKAGE_NAME user@system-ip:/path/"
    echo
    echo "2. SSH to the system:"
    echo "   ssh user@system-ip"
    echo
    echo "3. Extract and run:"
    echo "   tar -xzf $PACKAGE_NAME"
    echo "   cd vision_qa_deployment"
    echo "   chmod +x start_vision_app.sh"
    echo "   ./start_vision_app.sh"
    echo
    echo "=================================================="
    echo "  Ready for deployment to 12 systems! 🚀"
    echo "=================================================="
else
    echo "❌ Error: Failed to create package"
    exit 1
fi
