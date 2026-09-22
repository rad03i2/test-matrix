# Test Matrix

A small, deterministic Python tool for generating, filtering, validating, and exporting CI test matrices from a JSON specification.

## English

### Overview
CI matrices become difficult to review when operating systems, language versions, runtimes, and special cases multiply. Test Matrix keeps that logic in a portable JSON file, expands the Cartesian product deterministically, applies exclusions/additions, checks required coverage, and can emit a GitHub Actions-compatible explicit `include` matrix.

### Why it exists
The project provides one testable source of truth for matrix policy without requiring a CI provider SDK. It is useful for previewing combinations locally, guarding against missing supported platforms, and feeding generated JSON into automation.

### Key features
- Deterministic Cartesian matrix generation with stable axis/value order.
- Partial-match `exclude` rules and explicit `include` additions.
- Coverage assertions through a `required` section.
- Human-readable rows, structured JSON, and GitHub Actions `include` output.
- Resource guard: 10,000 combinations by default, configurable downward or upward.
- Reads UTF-8 JSON files or stdin (`-`); no network, credentials, telemetry, or runtime dependencies.
- Python API plus installable `test-matrix` CLI.
- Distinct exit codes: `0` success, `1` invalid input/configuration, `2` coverage failure.

### Preview
No graphical UI is required. Try the included example:

```console
$ test-matrix examples/matrix.json --format github --check-coverage
{
  "include": [
    {"python": "3.10", "os": "ubuntu-latest"},
    ...
  ]
}
```

### Requirements and installation
Requires Python 3.10 or newer.

```bash
python -m pip install -e .
test-matrix --version
```

For development:

```bash
python -m pip install -e . pytest
```

### Specification and usage
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
type examples\matrix.json | test-matrix - --format github   # Windows
a cat examples/matrix.json 2>/dev/null || true              # not required; shell-specific example omitted intentionally
```

On POSIX shells, stdin is simply `cat examples/matrix.json | test-matrix - --format github`.

`--max-combinations N` changes the expansion safety ceiling. `--check-coverage` checks values under `required` after include/exclude processing.

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

### Security and privacy
Input is treated as data: Test Matrix does not execute commands contained in specifications. It makes no network requests and stores nothing. The combination ceiling reduces accidental memory/CPU blow-ups. For hostile inputs, use a smaller ceiling and normal OS-level resource controls.

### Limitations
- JSON is the only specification format; YAML/TOML are not parsed.
- `exclude` is exact value matching on the keys present in a rule; expressions and wildcards are intentionally unsupported.
- `include` entries are appended as explicit rows and may contain keys outside the declared axes.
- GitHub output is an explicit `include` matrix; the tool does not edit workflow files or call GitHub APIs.
- Coverage checks verify that required individual values occur, not pairwise or N-wise combinatorial coverage.

### Optional roadmap
Potential future work includes pairwise coverage assertions and additional export formats, provided determinism and a small dependency footprint are preserved.

### Contributing and license
See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Test Matrix** أداة بايثون صغيرة وحتمية لتوليد مصفوفات الاختبار الخاصة بأنظمة CI من ملف JSON. توسّع المحاور إلى جميع التركيبات، ثم تطبق الاستثناءات والإضافات، وتتحقق من تغطية القيم المطلوبة، ويمكنها إخراج مصفوفة `include` متوافقة مع GitHub Actions.

### لماذا هذا المشروع؟
عندما تتعدد أنظمة التشغيل وإصدارات اللغات والبيئات تصبح مصفوفة CI صعبة المراجعة. يوفر المشروع ملف سياسة واحدًا قابلًا للاختبار والمعاينة محليًا دون الاعتماد على SDK خاص بمنصة CI.

### الميزات
- توليد Cartesian Product بترتيب ثابت وقابل للتكرار.
- قواعد `exclude` بالمطابقة الجزئية وإضافات `include` الصريحة.
- فحص التغطية بواسطة قسم `required`.
- إخراج جدولي أو JSON أو صيغة GitHub Actions.
- حد أمان افتراضي قدره 10,000 تركيبة لمنع التوسع غير المقصود.
- قراءة JSON بترميز UTF-8 من ملف أو stdin، بلا شبكة أو أسرار أو telemetry أو اعتماديات تشغيل خارجية.
- CLI باسم `test-matrix` وواجهة Python API.
- رموز خروج واضحة: 0 للنجاح، 1 للمدخل غير الصحيح، و2 لفشل التغطية.

### المعاينة والتثبيت
لا يحتاج المشروع إلى واجهة رسومية. يتطلب Python 3.10 أو أحدث:

```bash
python -m pip install -e .
test-matrix examples/matrix.json --format github --check-coverage
```

### الاستخدام والإعداد
يتضمن ملف المواصفات `axes` ويمكن أن يتضمن `exclude` و`include` و`required`. المثال الكامل موجود في `examples/matrix.json`.

```bash
test-matrix examples/matrix.json
test-matrix examples/matrix.json --format json --check-coverage
test-matrix examples/matrix.json --format github
```

يمكن تغيير حد التركيبات عبر `--max-combinations N`. وفحص `--check-coverage` يتم بعد تطبيق الاستثناءات والإضافات.

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
ويختبر CI الإصدارات 3.10 و3.12 و3.13 على Ubuntu وWindows وmacOS.

### الأمان والخصوصية
الأداة تقرأ المواصفات كبيانات فقط ولا تنفذ أوامر منها، ولا تتصل بالشبكة ولا تخزن بيانات. حد التركيبات يقلل خطر استهلاك الموارد غير المقصود. للمدخلات غير الموثوقة يفضل استخدام حد أصغر مع قيود موارد النظام.

### القيود
يدعم الإصدار الحالي JSON فقط، ولا يدعم التعبيرات أو wildcards في الاستثناءات. صيغة GitHub هي مصفوفة `include` صريحة ولا تعدل ملفات workflow ولا تستدعي GitHub API. فحص التغطية يتحقق من ظهور كل قيمة مطلوبة منفردة، وليس pairwise أو N-wise coverage.

### تطوير اختياري
يمكن مستقبلًا إضافة فحص pairwise وصيغ تصدير أخرى بشرط الحفاظ على الحتمية وبساطة الاعتماديات.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) و[SECURITY.md](SECURITY.md). المشروع مرخص وفق [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
