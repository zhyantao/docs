pip install clang-format==18.1.8
SITE_PACKAGES_DIR=$(python -c "import site; print('\n'.join(site.getsitepackages()));")
find . -type f \( -name "*.cpp" -o -name "*.c" -o -name "*.cc" -o -name "*.h" -o -name "*.hpp" \) \
-not -path "./.git/*" \
-not -path "./.svn/*" \
-not -path "./.github/*" \
-exec $SITE_PACKAGES_DIR/clang_format/data/bin/clang-format -i {} +
