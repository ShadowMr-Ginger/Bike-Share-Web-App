import requests
import json
from packaging import version

def check_package_compatibility(package_name, package_version):
    """Check if a package version supports Python 3.14"""
    try:
        # Query PyPI API
        url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            # Try without version to get latest info
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return None, "Failed to fetch package info"
        
        data = response.json()
        
        # Get classifiers
        classifiers = data.get('info', {}).get('classifiers', [])
        
        # Extract Python version classifiers
        python_versions = []
        for classifier in classifiers:
            if classifier.startswith('Programming Language :: Python :: 3'):
                python_versions.append(classifier)
        
        # Check for Python 3.14 support
        has_314 = any('3.14' in v for v in python_versions)
        has_313 = any('3.13' in v for v in python_versions)
        has_312 = any('3.12' in v for v in python_versions)
        
        # Get requires_python field
        requires_python = data.get('info', {}).get('requires_python', '')
        
        return {
            'python_versions': python_versions,
            'has_314': has_314,
            'has_313': has_313,
            'has_312': has_312,
            'requires_python': requires_python
        }, None
        
    except Exception as e:
        return None, str(e)

def main():
    # Read requirements.txt
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    
    incompatible_packages = []
    compatible_packages = []
    unknown_packages = []
    
    print("Checking Python 3.14 compatibility for packages in requirements.txt...\n")
    print("=" * 80)
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Parse package name and version
        if '==' in line:
            package_name, package_version = line.split('==')
        else:
            package_name = line
            package_version = None
        
        print(f"\nChecking: {package_name} {package_version or '(latest)'}")
        
        result, error = check_package_compatibility(package_name, package_version)
        
        if error:
            print(f"  ❓ Error: {error}")
            unknown_packages.append((package_name, package_version, error))
        elif result:
            if result['has_314']:
                print(f"  ✅ Supports Python 3.14")
                compatible_packages.append((package_name, package_version))
            else:
                status = []
                if result['has_313']:
                    status.append("3.13")
                if result['has_312']:
                    status.append("3.12")
                
                max_supported = ", ".join(status) if status else "Unknown"
                print(f"  ⚠️  Does NOT explicitly support Python 3.14")
                print(f"     Latest supported: {max_supported}")
                print(f"     Requires Python: {result['requires_python'] or 'Not specified'}")
                incompatible_packages.append((package_name, package_version, max_supported, result['requires_python']))
    
    # Summary
    print("\n" + "=" * 80)
    print("\n📊 SUMMARY:")
    print(f"  ✅ Compatible with Python 3.14: {len(compatible_packages)}")
    print(f"  ⚠️  NOT explicitly supporting Python 3.14: {len(incompatible_packages)}")
    print(f"  ❓ Unknown/Error: {len(unknown_packages)}")
    
    if incompatible_packages:
        print("\n" + "=" * 80)
        print("\n⚠️  PACKAGES NOT EXPLICITLY SUPPORTING PYTHON 3.14:")
        print("-" * 80)
        for pkg_name, pkg_ver, max_sup, req_py in incompatible_packages:
            print(f"  • {pkg_name}=={pkg_ver}")
            print(f"    Latest supported: {max_sup}")
            print(f"    Requires Python: {req_py or 'Not specified'}")
    
    if unknown_packages:
        print("\n" + "=" * 80)
        print("\n❓ PACKAGES WITH ERRORS:")
        print("-" * 80)
        for pkg_name, pkg_ver, err in unknown_packages:
            print(f"  • {pkg_name}=={pkg_ver or 'latest'}: {err}")

if __name__ == "__main__":
    main()
