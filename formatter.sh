pip install -r requirements.txt
SITE_PACKAGES_DIR=$(python -c "import site; print(site.getsitepackages()[0]);")
find . -type f \( -name "*.cpp" -o -name "*.c" -o -name "*.cc" -o -name "*.h" -o -name "*.hpp" \) \
    -not -path "./.git/*" \
    -not -path "./.svn/*" \
    -not -path "./.github/*" \
    -exec $SITE_PACKAGES_DIR/clang_format/data/bin/clang-format -i {} +
