# Test Matrix

A small, deterministic Python tool for generating, filtering, validating, and exporting CI test matrices from a JSON specification.

## English

### Overview
CI matrices become difficult to review when operating systems, language versions, runtimes, and special cases multiply. Test Matrix keeps that logic in portable JSON, expands the Cartesian product deterministically, applies exclusions/additions, checks required coverage, and can emit a GitHub Actions-compatible explicit `include` matrix.

### Why it exists
It provides one testable source of truth for matrix policy without a CI-provider SDK: preview combinations locally, guard supported-platform coverage, and feed generated JSON into automation.

### Key features
- Deterministic Cartesian generation with stable axis/value order.
- Partial-match `exclude` rules and explicit `include` additions.
- Coverage assertions through `required`.
- Human-readable rows, structured JSON, and GitHub Actions `include` output.
- 10,000-combination resource guard by default, configurable with `--max-combinations`.
- UTF-8 JSON file or stdin input; no network, credentials, telemetry, or runtime dependencies.
- Python API and installable `test-matrix` CLI.
- Exit codes: `0` success, `1` invalid input/configuration, `2` coverage failure.

### Preview
```console
$ test-matrix examples/matrix.json --format github --check-coverage
{
  "include": [
    {"python": "3.10", "os": "ubuntu-latest"},
    ...
  ]
}
```
No graphical UI is required.

### Requirements & installation
Requires Python 3.10+.
```bash
python -m pip install -e .
test-matrix --version
```
For development: `python -m pip install -e . pytest`.

### Specification & usage
A specification contains `axes` and may contain `exclude`, `include`, and `required`:
```json
{
  "axes": {"python": ["3.11", "3.12"], "os": ["ubuntu", "windows"]},
  "exclude": [{"python": "3.11", "os": "windows"}],
  "include": [{"python": "3.13", "os": "ubuntu", "experimental": true}],
  "required": {"python": ["3.11", "3.12", "3.13"]}
}
```
```bash
test-matrix examples/matrix.json
test-matrix examples/matrix.json --format json --check-coverage
test-matrix examples/matrix.json --format github
```
POSIX stdin: `cat examples/matrix.json | test-matrix - --format github`  
Windows CMD stdin: `type examples\matrix.json | test-matrix - --format github`

`--check-coverage` checks `required` after include/exclude processing.

### Python API
```python
from test_matrix import generate_matrix, validate_coverage
result = generate_matrix({"python": ["3.11", "3.12"], "os": ["linux", "windows"]})
print(result.count)
print(result.as_github_matrix())
print(validate_coverage(result, {"os": ["linux", "windows"]}))
```

### Project structure
```text
src/test_matrix/      core engine, public API and CLI
tests/                core and CLI tests
examples/matrix.json  practical sample specification
.github/workflows/    cross-platform CI
```

### Testing
```bash
python -m pytest
python -m compileall -q src
test-matrix examples/matrix.json --format github --check-coverage
```
CI runs these checks on Python 3.10, 3.12 and 3.13 across Ubuntu, Windows and macOS.

### Security & privacy
Specifications are data only: commands in them are never executed. The tool makes no network requests and stores nothing. The combination ceiling reduces accidental memory/CPU blow-ups; use a smaller ceiling and OS resource controls for hostile inputs.

### Limitations
- JSON only; YAML/TOML are not parsed.
- `exclude` uses exact values on keys present in each rule; no expressions or wildcards.
- `include` rows may contain keys outside declared axes.
- GitHub output is explicit `include`; the tool does not edit workflows or call GitHub APIs.
- Coverage checks individual values, not pairwise/N-wise combinatorial coverage.

### Optional roadmap
Pairwise coverage assertions and more export formats are reasonable future additions if determinism and the small dependency footprint are preserved.

### Contributing & license
See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Test Matrix** أداة بايثون صغيرة وحتمية لتوليد مصفوفات الاختبار الخاصة بأنظمة CI من JSON. توسّع المحاور إلى جميع التركيبات، ثم تطبق الاستثناءات والإضافات، وتتحقق من تغطية القيم المطلوبة، ويمكنها إخراج مصفوفة `include` متوافقة مع GitHub Actions.

### لماذا هذا المشروع؟
عندما تتعدد أنظمة التشغيل وإصدارات اللغات تصبح مصفوفة CI صعبة المراجعة. يوفر المشروع مصدر سياسة واحدًا قابلًا للاختبار والمعاينة محليًا دون SDK خاص بمنصة CI.

### الميزات
- Cartesian Product بترتيب ثابت وقابل للتكرار.
- `exclude` بالمطابقة الجزئية و`include` للإضافات الصريحة.
- فحص التغطية بواسطة `required`.
- إخراج جدولي أو JSON أو GitHub Actions.
- حد أمان افتراضي 10,000 تركيبة قابل للتعديل.
- قراءة UTF-8 JSON من ملف أو stdin، بلا شبكة أو أسرار أو telemetry أو اعتماديات تشغيل خارجية.
- CLI باسم `test-matrix` وPython API.
- رموز خروج: 0 نجاح، 1 مدخل غير صحيح، 2 فشل التغطية.

### المعاينة والمتطلبات والتثبيت
لا يحتاج المشروع إلى واجهة رسومية، ويتطلب Python 3.10+.
```bash
python -m pip install -e .
test-matrix examples/matrix.json --format github --check-coverage
```

### الاستخدام والإعداد
المثال الكامل في `examples/matrix.json`.
```bash
test-matrix examples/matrix.json
test-matrix examples/matrix.json --format json --check-coverage
test-matrix examples/matrix.json --format github
```
يمكن تغيير حد التركيبات عبر `--max-combinations N`. ويتم `--check-coverage` بعد الاستثناءات والإضافات.

### Python API
```python
from test_matrix import generate_matrix
result = generate_matrix({"python": ["3.11", "3.12"], "os": ["linux", "windows"]})
print(result.as_github_matrix())
```

### بنية المشروع
`src/test_matrix/` للمحرك والـCLI، و`tests/` للاختبارات، و`examples/` للأمثلة، و`.github/workflows/` للتكامل المستمر.

### الاختبارات
```bash
python -m pytest
python -m compileall -q src
test-matrix examples/matrix.json --format github --check-coverage
```
ويختبر CI Python 3.10 و3.12 و3.13 على Ubuntu وWindows وmacOS.

### الأمان والخصوصية
تقرأ الأداة المواصفات كبيانات فقط ولا تنفذ أوامر منها، ولا تتصل بالشبكة ولا تخزن بيانات. حد التركيبات يقلل استهلاك الموارد غير المقصود؛ استخدم حدًا أصغر مع المدخلات غير الموثوقة.

### القيود
يدعم الإصدار الحالي JSON فقط، ولا يدعم التعبيرات أو wildcards في الاستثناءات. صيغة GitHub هي `include` صريحة ولا تعدل workflow ولا تستدعي GitHub API. فحص التغطية يتحقق من ظهور كل قيمة مطلوبة منفردة وليس pairwise أو N-wise coverage.

### تطوير اختياري
يمكن إضافة فحص pairwise وصيغ تصدير أخرى مستقبلًا بشرط الحفاظ على الحتمية وبساطة الاعتماديات.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) و[SECURITY.md](SECURITY.md). المشروع مرخص وفق [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
