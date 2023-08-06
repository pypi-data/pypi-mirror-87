import difflib
from mys.parser import ast
import sys
import unittest
from mys.transpile import transpile
from mys.transpile import Source
from mys.definitions import find_definitions

from .utils import read_file
from .utils import remove_ansi

def transpile_header(source, filename='', module_hpp=''):
    return transpile([Source(source,
                             filename=filename,
                             module_hpp=module_hpp)])[0][0]

def transpile_source(source, filename='', module_hpp=''):
    return transpile([Source(source,
                             filename=filename,
                             module_hpp=module_hpp)])[0][1]


class MysTest(unittest.TestCase):

    maxDiff = None

    def assert_equal_to_file(self, actual, expected):
        # open(expected, 'w').write(actual)
        self.assertEqual(read_file(expected), actual)

    def assert_in(self, needle, haystack):
        try:
            self.assertIn(needle, haystack)
        except AssertionError:
            differ = difflib.Differ()
            diff = differ.compare(needle.splitlines(), haystack.splitlines())

            raise AssertionError(
                '\n' + '\n'.join([diffline.rstrip('\n') for diffline in diff]))

    def test_all(self):
        datas = [
            'basics'
        ]

        for data in datas:
            header, source = transpile([
                Source(read_file(f'tests/files/{data}.mys'),
                       filename=f'{data}.mys',
                       module_hpp=f'{data}.mys.hpp')
            ])[0]
            self.assert_equal_to_file(
                header,
                f'tests/files/{data}.mys.hpp')
            self.assert_equal_to_file(
                source,
                f'tests/files/{data}.mys.cpp')

    def test_invalid_main_argument(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def main(argv: i32): pass')

        self.assertEqual(str(cm.exception),
                         "main() takes 'argv: [string]' or no arguments.")

    def test_invalid_main_return_type(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def main() -> i32: pass')

        self.assertEqual(str(cm.exception), "main() must return 'None'.")

    def test_lambda_not_supported(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def main(): print((lambda x: x)(1))',
                             filename='foo.py')

        self.assertEqual(remove_ansi(str(cm.exception)),
                         '  File "foo.py", line 1\n'
                         '    def main(): print((lambda x: x)(1))\n'
                         '                       ^\n'
                         'LanguageError: lambda functions are not supported\n')

    def test_bad_syntax(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('DEF main(): pass', filename='<unknown>')

        self.assertEqual(remove_ansi(str(cm.exception)),
                         '  File "<unknown>", line 1\n'
                         '    DEF main(): pass\n'
                         '        ^\n'
                         'SyntaxError: invalid syntax\n')

    def test_import_in_function_should_fail(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def main():\n'
                             '    import foo\n',
                             filename='<unknown>')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "<unknown>", line 2\n'
            '        import foo\n'
            '        ^\n'
            'LanguageError: imports are only allowed on module level\n')

    def test_class_in_function_should_fail(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def main():\n'
                             '    class A:\n'
                             '        pass\n',
                             filename='<unknown>')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "<unknown>", line 2\n'
            '        class A:\n'
            '        ^\n'
            'LanguageError: class definitions are only allowed on module level\n')

    def test_empty_function(self):
        source = transpile_source('def foo():\n'
                                  '    pass\n')

        self.assert_in('void foo(void)\n'
                       '{\n'
                       '\n'
                       '}\n',
                       source)

    def test_multiple_imports_failure(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('from foo import bar, fie\n',
                             filename='<unknown>')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "<unknown>", line 1\n'
            '    from foo import bar, fie\n'
            '    ^\n'
            'LanguageError: only one import is allowed, found 2\n')

    def test_relative_import_outside_package(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('from .. import fie\n',
                             filename='src/mod.mys',
                             module_hpp='pkg/mod.mys.hpp')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "src/mod.mys", line 1\n'
            '    from .. import fie\n'
            '    ^\n'
            'LanguageError: relative import is outside package\n')

    def test_comaprsion_operator_return_types(self):
        ops = ['eq', 'ne', 'gt', 'ge', 'lt', 'le']

        for op in ops:
            with self.assertRaises(Exception) as cm:
                transpile_source('class Foo:\n'
                                 f'    def __{op}__(self, other: Foo):\n'
                                 '        return True\n',
                                 filename='src/mod.mys',
                                 module_hpp='pkg/mod.mys.hpp')

            self.assertEqual(
                remove_ansi(str(cm.exception)),
                '  File "src/mod.mys", line 2\n'
                f'        def __{op}__(self, other: Foo):\n'
                '        ^\n'
                f'LanguageError: __{op}__() must return bool\n')

    def test_arithmetic_operator_return_types(self):
        ops = ['add', 'sub']

        for op in ops:
            with self.assertRaises(Exception) as cm:
                transpile_source('class Foo:\n'
                                 f'    def __{op}__(self, other: Foo) -> bool:\n'
                                 '        return True\n',
                                 'src/mod.mys',
                                 'pkg/mod.mys.hpp')

            self.assertEqual(
                remove_ansi(str(cm.exception)),
                '  File "src/mod.mys", line 2\n'
                f'        def __{op}__(self, other: Foo) -> bool:\n'
                '        ^\n'
                f'LanguageError: __{op}__() must return Foo\n')

    def test_basic_print_function(self):
        source = transpile_source('def main():\n'
                                  '    print("Hi!")\n')

        self.assert_in('std::cout << "Hi!" << std::endl;', source)

    def test_print_function_with_end(self):
        source = transpile_source('def main():\n'
                                  '    print("Hi!", end="")\n')

        self.assert_in('std::cout << "Hi!" << "";', source)

    def test_print_function_with_flush_true(self):
        source = transpile_source('def main():\n'
                                  '    print("Hi!", flush=True)\n')

        self.assert_in('    std::cout << "Hi!" << std::endl;\n'
                       '    if (true) {\n'
                       '        std::cout << std::flush;\n'
                       '    }',
                       source)


    def test_print_function_with_flush_false(self):
        source = transpile_source('def main():\n'
                                  '    print("Hi!", flush=False)\n')

        self.assert_in('std::cout << "Hi!" << std::endl;', source)

    def test_print_function_with_and_and_flush(self):
        source = transpile_source('def main():\n'
                                  '    print("Hi!", end="!!", flush=True)\n')

        self.assert_in('    std::cout << "Hi!" << "!!";\n'
                       '    if (true) {\n'
                       '        std::cout << std::flush;\n'
                       '    }',
                       source)

    def test_print_function_invalid_keyword(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def main():\n'
                             '    print("Hi!", foo=True)\n',
                             'src/mod.mys',
                             'pkg/mod.mys.hpp')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "src/mod.mys", line 2\n'
            '        print("Hi!", foo=True)\n'
            '        ^\n'
            "LanguageError: invalid keyword argument 'foo' to print(), only "
            "'end' and 'flush' are allowed\n")

    def test_undefined_variable_1(self):
        # Everything ok, 'value' defined.
        transpile_source('def foo(value: bool) -> bool:\n'
                         '    return value\n')

        # Error, 'value' is not defined.
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo() -> bool:\n'
                             '    return value\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        return value\n'
            '               ^\n'
            "LanguageError: undefined variable 'value'\n")

    def test_undefined_variable_2(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo() -> i32:\n'
                             '    return 2 * value\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        return 2 * value\n'
            '                   ^\n'
            "LanguageError: undefined variable 'value'\n")

    def test_undefined_variable_3(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo(v1: i32) -> i32:\n'
                             '    return v1\n'
                             'def bar() -> i32:\n'
                             '    a: i32 = 1\n'
                             '    return foo(a, value)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 5\n'
            '        return foo(a, value)\n'
            '                      ^\n'
            "LanguageError: undefined variable 'value'\n")

    def test_undefined_variable_4(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def bar():\n'
                             '    try:\n'
                             '        pass\n'
                             '    except Exception as e:\n'
                             '        pass\n'
                             '\n'
                             '    print(e)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 7\n'
            '        print(e)\n'
            '              ^\n'
            "LanguageError: undefined variable 'e'\n")

    def test_undefined_variable_in_fstring(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def bar():\n'
                             '    print(f"{value}")\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        print(f"{value}")\n'
            '                 ^\n'
            "LanguageError: undefined variable 'value'\n")

    def test_only_global_defined_in_callee(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('glob: bool = True\n'
                             'def bar() -> i32:\n'
                             '    a: i32 = 1\n'
                             '    return foo(a)\n'
                             'def foo(v1: i32) -> i32:\n'
                             '    return glob + v1 + a\n'
                             '')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 6\n'
            '        return glob + v1 + a\n'
            '                           ^\n'
            "LanguageError: undefined variable 'a'\n")

    def test_imported_variable_usage(self):
        transpile([
            Source('from foo import bar\n'
                   '\n'
                   'def fie() -> i32:\n'
                   '    return 2 * bar\n'),
            Source('bar: i32 = 1', module='foo.lib')
        ])

    def test_imported_module_does_not_exist(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('from foo import bar\n'
                             '\n'
                             'def fie() -> i32:\n'
                             '    return 2 * bar\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    from foo import bar\n'
            '    ^\n'
            "LanguageError: imported module 'foo.lib' does not exist\n")

    def test_imported_module_does_not_contain(self):
        with self.assertRaises(Exception) as cm:
            transpile([
                Source('from foo import bar\n'
                       '\n'
                       'def fie() -> i32:\n'
                       '    return 2 * bar\n'),
                Source('boo: i32 = 1', module='foo.lib')
            ])

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    from foo import bar\n'
            '    ^\n'
            "LanguageError: imported module 'foo.lib' does not contain 'bar'\n")

    def test_import_private_function_fails(self):
        with self.assertRaises(Exception) as cm:
            transpile([
                Source('from foo import _bar\n'
                       '\n'
                       'def fie() -> i32:\n'
                       '    return 2 * _bar\n'),
                Source('_bar: i32 = 1', module='foo.lib')
            ])

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    from foo import _bar\n'
            '    ^\n'
            "LanguageError: can't import private definition '_bar'\n")

    def test_find_definitions(self):
        definitions = find_definitions(
            ast.parse(
                'VAR1: i32 = 1\n'
                '_VAR2: [bool] = [True, False]\n'
                '@enum\n'
                'class Enum1:\n'
                '    A\n'
                '    B\n'
                '    C\n'
                '    D = 100\n'
                '    E\n'
                '@enum(u8)\n'
                'class _Enum2:\n'
                '    Aa = 1\n'
                '    Bb = -5\n'
                '@trait\n'
                'class Trait1:\n'
                '    def foo(self):\n'
                '        pass\n'
                'class Class1:\n'
                '    m1: i32\n'
                '    m2: [i32]\n'
                '    _m3: i32\n'
                '    def foo(self):\n'
                '        pass\n'
                '    def bar(self, a: i32) -> i32:\n'
                '        return a\n'
                '    def bar(self, a: i32, b: (bool, u8)) -> [i32]:\n'
                '        return a\n'
                '    def fie(a: i32):\n'
                '        pass\n'
                'class Class2:\n'
                '    pass\n'
                '@generic(T)\n'
                'class _Class3:\n'
                '    a: T\n'
                'def func1(a: i32, b: bool, c: Class1, d: [(u8, string)]):\n'
                '    pass\n'
                'def func2() -> bool:\n'
                '    pass\n'
                '@raises(TypeError)\n'
                'def func3() -> [i32]:\n'
                '    raise TypeError()\n'
                '@generic(T1, T2)\n'
                'def _func4(a: T1, b: T2):\n'
                '    pass\n'))

        self.assertEqual(list(definitions.variables), ['VAR1', '_VAR2'])
        self.assertEqual(list(definitions.classes), ['Class1', 'Class2', '_Class3'])
        self.assertEqual(list(definitions.traits), ['Trait1'])
        self.assertEqual(list(definitions.functions),
                         ['func1', 'func2', 'func3', '_func4'])
        self.assertEqual(list(definitions.enums), ['Enum1', '_Enum2'])

        # Variables.
        var1 = definitions.variables['VAR1']
        self.assertEqual(var1, 'i32')

        var2 = definitions.variables['_VAR2']
        self.assertEqual(var2, ['bool'])

        # Enums.
        enum1 = definitions.enums['Enum1']
        self.assertEqual(enum1.name, 'Enum1')
        self.assertEqual(enum1.type, 'i64')
        self.assertEqual(enum1.members,
                         [('A', 0), ('B', 1), ('C', 2), ('D', 100), ('E', 101)])

        enum2 = definitions.enums['_Enum2']
        self.assertEqual(enum2.name, '_Enum2')
        self.assertEqual(enum2.type, 'u8')
        self.assertEqual(enum2.members, [('Aa', 1), ('Bb', -5)])

        # Functions.
        func1s = definitions.functions['func1']
        self.assertEqual(len(func1s), 1)

        func1 = func1s[0]
        self.assertEqual(func1.name, 'func1')
        self.assertEqual(func1.returns, None)
        self.assertEqual(
            func1.args,
            [('a', 'i32'), ('b', 'bool'), ('c', 'Class1'), ('d', [('u8', 'string')])])

        func2s = definitions.functions['func2']
        self.assertEqual(len(func2s), 1)

        func2 = func2s[0]
        self.assertEqual(func2.name, 'func2')
        self.assertEqual(func2.returns, 'bool')
        self.assertEqual(func2.args, [])

        func3s = definitions.functions['func3']
        self.assertEqual(len(func3s), 1)

        func3 = func3s[0]
        self.assertEqual(func3.name, 'func3')
        self.assertEqual(func3.raises, ['TypeError'])
        self.assertEqual(func3.returns, ['i32'])
        self.assertEqual(func3.args, [])

        func4s = definitions.functions['_func4']
        self.assertEqual(len(func4s), 1)

        func4 = func4s[0]
        self.assertEqual(func4.name, '_func4')
        self.assertEqual(func4.generic_types, ['T1', 'T2'])
        self.assertEqual(func4.returns, None)
        self.assertEqual(func4.args, [('a', 'T1'), ('b', 'T2')])

        # Class1.
        class1 = definitions.classes['Class1']
        self.assertEqual(class1.name, 'Class1')
        self.assertEqual(class1.generic_types, [])
        self.assertEqual(list(class1.members), ['m1', 'm2', '_m3'])
        self.assertEqual(list(class1.methods), ['foo', 'bar'])
        self.assertEqual(list(class1.functions), ['fie'])

        # Members.
        m1 = class1.members['m1']
        self.assertEqual(m1.name, 'm1')
        self.assertEqual(m1.type, 'i32')

        m2 = class1.members['m2']
        self.assertEqual(m2.name, 'm2')
        self.assertEqual(m2.type, ['i32'])

        m3 = class1.members['_m3']
        self.assertEqual(m3.name, '_m3')
        self.assertEqual(m3.type, 'i32')

        # Methods.
        foos = class1.methods['foo']
        self.assertEqual(len(foos), 1)

        foo = foos[0]
        self.assertEqual(foo.name, 'foo')
        self.assertEqual(foo.returns, None)
        self.assertEqual(foo.args, [])

        bars = class1.methods['bar']
        self.assertEqual(len(bars), 2)

        bar = bars[0]
        self.assertEqual(bar.name, 'bar')
        self.assertEqual(bar.returns, 'i32')
        self.assertEqual(bar.args, [('a', 'i32')])

        bar = bars[1]
        self.assertEqual(bar.name, 'bar')
        self.assertEqual(bar.returns, ['i32'])
        self.assertEqual(bar.args, [('a', 'i32'), ('b', ('bool', 'u8'))])

        fies = class1.functions['fie']
        self.assertEqual(len(fies), 1)

        # Functions.
        fie = fies[0]
        self.assertEqual(fie.name, 'fie')
        self.assertEqual(fie.returns, None)
        self.assertEqual(fie.args, [('a', 'i32')])

        # _Class3.
        class3 = definitions.classes['_Class3']
        self.assertEqual(class3.name, '_Class3')
        self.assertEqual(class3.generic_types, ['T'])
        self.assertEqual(list(class3.members), ['a'])
        self.assertEqual(list(class3.methods), [])
        self.assertEqual(list(class3.functions), [])

        # Members.
        a = class3.members['a']
        self.assertEqual(a.name, 'a')
        self.assertEqual(a.type, 'T')

        # Trait1.
        trait1 = definitions.traits['Trait1']
        self.assertEqual(trait1.name, 'Trait1')
        self.assertEqual(list(trait1.methods), ['foo'])

        # Methods.
        foos = trait1.methods['foo']
        self.assertEqual(len(foos), 1)

        foo = foos[0]
        self.assertEqual(foo.name, 'foo')
        self.assertEqual(foo.returns, None)
        self.assertEqual(foo.args, [])

    def test_test_decorator_only_allowed_on_functions(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('class Class1:\n'
                             '    @test\n'
                             '    def foo(self):\n'
                             '        pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        @test\n'
            '         ^\n'
            "LanguageError: invalid decorator 'test'\n")

    def test_missing_generic_type(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@generic\n'
                             'def foo():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @generic\n'
            '     ^\n'
            "LanguageError: @generic requires at least one type\n")

    def test_missing_errors_in_raises(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@raises()\n'
                             'def foo():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @raises()\n'
            '     ^\n'
            "LanguageError: @raises requires at least one error\n")

    def test_generic_given_more_than_once(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@generic(T1)\n'
                             '@generic(T2)\n'
                             'def foo(a: T1, b: T2):\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '    @generic(T2)\n'
            '     ^\n'
            "LanguageError: @generic can only be given once\n")

    def test_generic_type_given_more_than_once(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@generic(T1, T1)\n'
                             'def foo(a: T1):\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @generic(T1, T1)\n'
            '                 ^\n'
            "LanguageError: 'T1' can only be given once\n")

    def test_test_can_not_take_any_values(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@test(H)\n'
                             'def foo():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @test(H)\n'
            '     ^\n'
            "LanguageError: @test does not take any values\n")

    def test_non_snake_case_function(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def Apa():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    def Apa():\n'
            '    ^\n'
            "LanguageError: function names must be snake case\n")

    def test_non_snake_case_global_variable(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('Aa: i32 = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    Aa: i32 = 1\n'
            '    ^\n'
            "LanguageError: variable names must be upper or lower case snake case\n")

    def test_non_snake_case_class_member(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('class A:\n'
                             '    Aa: i32')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        Aa: i32\n'
            '        ^\n'
            "LanguageError: class member names must be snake case\n")

    def test_non_pascal_case_class(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('class apa():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    class apa():\n'
            '    ^\n'
            "LanguageError: class names must be pascal case\n")

    def test_non_snake_case_function_parameter_name(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo(A: i32):\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    def foo(A: i32):\n'
            '            ^\n'
            "LanguageError: parameter names must be snake case\n")

    def test_non_snake_case_local_variable(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    A: i32 = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        A: i32 = 1\n'
            '        ^\n'
            "LanguageError: local variable names must be snake case\n")

    def test_for_loop_underscore_variable(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    for _ in [1, 4]:\n'
                             '        print(_)\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '            print(_)\n'
            '                  ^\n'
            "LanguageError: undefined variable '_'\n")

    def test_underscore_variable_name(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    _: i32 = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        _: i32 = 1\n'
            '        ^\n'
            "LanguageError: local variable names must be snake case\n")

    def test_underscore_inferred_variable_name(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    _ = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        _ = 1\n'
            '        ^\n'
            "LanguageError: local variable names must be snake case\n")

    def test_for_loop_underscores(self):
        source = transpile_source('def foo():\n'
                                  '    for _, _ in [(1, True)]:\n'
                                  '        pass\n')

        self.assertRegex(source,
                         r'for \(auto \[_\d+, _\d+\]: ')

    def test_non_snake_case_local_inferred_variable(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo():\n'
                             '    A = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 2\n'
            '        A = 1\n'
            '        ^\n'
            "LanguageError: local variable names must be snake case\n")

    def test_missing_function_parameter_type(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo(x):\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    def foo(x):\n'
            '            ^\n'
            "LanguageError: parameters must have a type\n")

    def test_invalid_decorator_value(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@raises(A(B))\n'
                             'def foo():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @raises(A(B))\n'
            '            ^\n'
            "LanguageError: invalid decorator value\n")

    def test_invalid_decorator_value_syntax(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@raises[A]\n'
                             'def foo():\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @raises[A]\n'
            '     ^\n'
            "LanguageError: decorators must be @name or @name()\n")

    def test_invalid_string_enum_member_value(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@enum\n'
                             'class Foo:\n'
                             '    A = "s"\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '        A = "s"\n'
            '            ^\n'
            "LanguageError: invalid enum member value\n")

    def test_invalid_enum_member_name(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@enum\n'
                             'class Foo:\n'
                             '    V1, V2 = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '        V1, V2 = 1\n'
            '        ^\n'
            "LanguageError: invalid enum member name\n")

    def test_invalid_enum_member_value_plus_sign(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@enum\n'
                             'class Foo:\n'
                             '    A = +1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '        A = +1\n'
            '            ^\n'
            "LanguageError: invalid enum member value\n")

    def test_invalid_enum_member_value_variable(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@enum\n'
                             'class Foo:\n'
                             '    A = b\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '        A = b\n'
            '            ^\n'
            "LanguageError: invalid enum member value\n")

    def test_non_pascal_case_enum_member_name(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@enum\n'
                             'class Foo:\n'
                             '    aB = 1\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '        aB = 1\n'
            '        ^\n'
            "LanguageError: enum member names must be pascal case\n")

    def test_define_empty_trait(self):
        source = transpile_source('@trait\n'
                                  'class Foo:\n'
                                  '    pass\n')
        self.assert_in('class Foo : public Object {\n'
                       '\n'
                       'public:\n'
                       '\n'
                       '};\n',
                       source)

    def test_define_trait_with_single_method(self):
        source = transpile_source('@trait\n'
                                  'class Foo:\n'
                                  '    def bar(self):\n'
                                  '        pass\n')

        self.assert_in('class Foo : public Object {\n'
                       '\n'
                       'public:\n'
                       '\n'
                       '    virtual void bar(void) = 0;\n'
                       '\n'
                       '};\n',
                       source)

    def test_define_trait_with_multiple_methods(self):
        source = transpile_source('@trait\n'
                                  'class Foo:\n'
                                  '    def bar(self):\n'
                                  '        pass\n'
                                  '    def fie(self, v1: i32) -> bool:\n'
                                  '        pass\n')

        self.assert_in('class Foo : public Object {\n'
                       '\n'
                       'public:\n'
                       '\n'
                       '    virtual void bar(void) = 0;\n'
                       '\n'
                       '    virtual bool fie(i32 v1) = 0;\n'
                       '\n'
                       '};\n',
                       source)

    def test_define_trait_with_method_body(self):
        # ToDo: Method bodies should eventually be supported, but not
        #       right now.
        with self.assertRaises(Exception) as cm:
            transpile_source('@trait\n'
                             'class Foo:\n'
                             '    def bar(self):\n'
                             '        print()\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 3\n'
            '        def bar(self):\n'
            '        ^\n'
            "LanguageError: trait method body must be 'pass'\n")

    def test_define_trait_with_same_name_twice(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@trait\n'
                             'class Foo:\n'
                             '    pass\n'
                             '@trait\n'
                             'class Foo:\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 5\n'
            '    class Foo:\n'
            '    ^\n'
            "LanguageError: there is already a trait called 'Foo'\n")

    def test_define_trait_with_same_name_as_class(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('class Foo:\n'
                             '    pass\n'
                             '@trait\n'
                             'class Foo:\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 4\n'
            '    class Foo:\n'
            '    ^\n'
            "LanguageError: there is already a class called 'Foo'\n")

    def test_implement_trait_in_class(self):
        source = transpile_source('@trait\n'
                                  'class Base:\n'
                                  '    def bar(self) -> bool:\n'
                                  '        pass\n'
                                  '@trait\n'
                                  'class Base2:\n'
                                  '    def fie(self):\n'
                                  '        pass\n'
                                  'class Foo(Base):\n'
                                  '    def bar(self) -> bool:\n'
                                  '        return False\n'
                                  'class Bar(Base, Base2):\n'
                                  '    def bar(self) -> bool:\n'
                                  '        return True\n'
                                  '    def fie(self):\n'
                                  '        print()\n')

        self.assert_in('class Foo : public Base {', source)
        self.assert_in('class Bar : public Base, public Base2 {', source)

    def test_trait_does_not_exist(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('class Foo(Bar):\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    class Foo(Bar):\n'
            '              ^\n'
            "LanguageError: trait does not exist\n")

    def test_invalid_decorator(self):
        with self.assertRaises(Exception) as cm:
            transpile_source('@foobar\n'
                             'class Foo:\n'
                             '    pass\n')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '    @foobar\n'
            '     ^\n'
            "LanguageError: invalid decorator 'foobar'\n")

    def test_match_i32(self):
        source = transpile_source('def foo(value: i32):\n'
                                  '    match value:\n'
                                  '        case 0:\n'
                                  '            print(value)\n'
                                  '        case _:\n'
                                  '            print(value)\n')

        self.assert_in('void foo(i32 value)\n'
                       '{\n'
                       '    if (value == 0) {\n'
                       '        std::cout << value << std::endl;\n'
                       '    } else {\n'
                       '        std::cout << value << std::endl;\n'
                       '    }\n'
                       '}',
                       source)

    def test_match_string(self):
        source = transpile_source('def foo(value: string):\n'
                                  '    match value:\n'
                                  '        case "a":\n'
                                  '            print(value)\n'
                                  '        case "b":\n'
                                  '            print(value)\n')

        self.assert_in('void foo(const String& value)\n'
                       '{\n'
                       '    if (value == "a") {\n'
                       '        std::cout << value << std::endl;\n'
                       '    } else if (value == "b") {\n'
                       '        std::cout << value << std::endl;\n'
                       '    }\n'
                       '}',
                       source)

    def test_match_function_return_value(self):
        source = transpile_source('def foo() -> i32:\n'
                                  '    return 1\n'
                                  'def bar():\n'
                                  '    match foo():\n'
                                  '        case 0:\n'
                                  '            print(0)\n')

        self.assertRegex(source,
                         r'void bar\(void\)\n'
                         r'{\n'
                         r'    auto subject_\d+ = foo\(\);\n'
                         r'    if \(subject_\d+ == 0\) {\n'
                         r'        std::cout << 0 << std::endl;\n'
                         r'    }\n'
                         r'}\n')

    def test_match_trait(self):
        source = transpile_source('@trait\n'
                                  'class Base:\n'
                                  '    pass\n'
                                  'class Foo(Base):\n'
                                  '    pass\n'
                                  'class Bar(Base):\n'
                                  '    pass\n'
                                  'class Fie(Base):\n'
                                  '    pass\n'
                                  'def foo(base: Base):\n'
                                  '    match base:\n'
                                  '        case Foo():\n'
                                  '            print("foo")\n'
                                  '        case Bar() as value:\n'
                                  '            print(value)\n'
                                  '        case Fie() as value:\n'
                                  '            print(value)\n')

        self.assertRegex(
            source,
            'void foo\(const std::shared_ptr<Base>& base\)\n'
            '{\n'
            '    auto casted_\d+ = std::dynamic_pointer_cast<Foo>\(base\);\n'
            '    if \(casted_\d+\) {\n'
            '        std::cout << "foo" << std::endl;\n'
            '    } else {\n'
            '        auto casted_\d+ = std::dynamic_pointer_cast<Bar>\(base\);\n'
            '        if \(casted_\d+\) {\n'
            '            auto value = std::move\(casted_\d+\);\n'
            '            std::cout << value << std::endl;\n'
            '        } else {\n'
            '            auto casted_\d+ = std::dynamic_pointer_cast<Fie>\(base\);\n'
            '            if \(casted_\d+\) {\n'
            '                auto value = std::move\(casted_\d+\);\n'
            '                std::cout << value << std::endl;\n'
            '            }\n'
            '        }\n'
            '    }\n'
            '}\n')

    def test_inferred_type_integer_assignment(self):
        source = transpile_source('def foo():\n'
                                  '    value_1 = 1\n'
                                  '    value_2 = -1\n'
                                  '    value_3 = +1\n'
                                  '    print(value_1, value_2, value_3)\n')

        self.assert_in(
            'void foo(void)\n'
            '{\n'
            '    i64 value_1 = 1;\n'
            '    i64 value_2 = -(1);\n'
            '    i64 value_3 = +(1);\n'
            '    std::cout << value_1 << " " << value_2 << " " << value_3 << std::endl;\n'
            '}\n',
            source)

    def test_inferred_type_string_assignment(self):
        source = transpile_source('def foo():\n'
                                  '    value = "a"\n'
                                  '    print(value)\n')

        self.assert_in('void foo(void)\n'
                       '{\n'
                       '    String value("a");\n'
                       '    std::cout << value << std::endl;\n'
                       '}\n',
                       source)

    def test_inferred_type_bool_assignment(self):
        source = transpile_source('def foo():\n'
                                  '    value = True\n'
                                  '    print(value)\n')

        self.assert_in('void foo(void)\n'
                       '{\n'
                       '    bool value = true;\n'
                       '    std::cout << value << std::endl;\n'
                       '}\n',
                       source)

    def test_inferred_type_float_assignment(self):
        source = transpile_source('def foo():\n'
                                  '    value = 6.44\n'
                                  '    print(value)\n')

        self.assert_in('void foo(void)\n'
                       '{\n'
                       '    f64 value = 6.44;\n'
                       '    std::cout << value << std::endl;\n'
                       '}\n',
                       source)

    def test_inferred_type_class_assignment(self):
        source = transpile_source('class A:\n'
                                  '    pass\n'
                                  'def foo():\n'
                                  '    value = A()\n'
                                  '    print(value)\n')

        self.assert_in('void foo(void)\n'
                       '{\n'
                       '    auto value = std::make_shared<A>();\n'
                       '    std::cout << value << std::endl;\n'
                       '}\n',
                       source)

    def test_string_as_function_parameter(self):
        source = transpile_source('def foo(value: string) -> string:\n'
                                  '    return value\n'
                                  'def bar():\n'
                                  '    print(foo("Cat"))\n')

        self.assert_in('void bar(void)\n'
                       '{\n'
                       '    std::cout << foo("Cat") << std::endl;\n'
                       '}\n',
                       source)

    def test_test_functions_not_in_header(self):
        header = transpile_header('@test\n'
                                  'def test_foo():\n'
                                  '    pass\n',
                                  module_hpp='foo/lib.mys.hpp')

        self.assertNotIn('test_foo', header)

    def test_function_header_signatures(self):
        header = transpile_header('class Foo:\n'
                                  '    pass\n'
                                  'def foo(a: i32, b: string, c: [i32]):\n'
                                  '    pass\n'
                                  'def bar(a: Foo) -> bool:\n'
                                  '    pass\n'
                                  'def fie(b: (i32, Foo)) -> u8:\n'
                                  '    pass\n'
                                  'def fum() -> [Foo]:\n'
                                  '    pass\n'
                                  'def fam() -> (bool, Foo):\n'
                                  '    pass\n')

        self.assert_in('void foo(i32 a, const String& b, List<i32>& c);', header)
        self.assert_in('bool bar(const std::shared_ptr<Foo>& a);', header)
        self.assert_in('u8 fie(Tuple<i32, const std::shared_ptr<Foo>>& b);', header)
        self.assert_in('List<Foo> fum(void);', header)
        self.assert_in('Tuple<bool, Foo> fam(void);', header)

    def test_function_source_signatures(self):
        source = transpile_source('class Foo:\n'
                                  '    pass\n'
                                  'def foo(a: i32, b: string, c: [i32]):\n'
                                  '    pass\n'
                                  'def bar(a: Foo) -> bool:\n'
                                  '    pass\n'
                                  'def fie(b: (i32, Foo)) -> u8:\n'
                                  '    pass\n'
                                  'def fum() -> [Foo]:\n'
                                  '    pass\n'
                                  'def fam() -> (bool, Foo):\n'
                                  '    pass\n')

        self.assert_in('void foo(i32 a, const String& b, List<i32>& c);', source)
        self.assert_in('bool bar(const std::shared_ptr<Foo>& a);', source)
        self.assert_in('u8 fie(Tuple<i32, const std::shared_ptr<Foo>>& b);', source)
        self.assert_in('List<Foo> fum(void);', source)
        self.assert_in('Tuple<bool, Foo> fam(void);', source)

    def test_enum_as_function_parameter_and_return_value(self):
        source = transpile_source(
            '@enum\n'
            'class City:\n'
            '\n'
            '    Linkoping = 5\n'
            '    Norrkoping = 8\n'
            '    Vaxjo = 10\n'
            'def enum_foo(source: City, destination: City) -> City:\n'
            '    return City.Vaxjo\n')

        self.assert_in(
            'i64 enum_foo(i64 source, i64 destination)\n'
            '{\n'
            '    return (i64)City::Vaxjo;\n'
            '}\n',
            source)

    # ToDo
    def test_return_i64_from_function_returning_string(self):
        return
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo() -> string:\n'
                             '    return 1')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '        return 1\n'
            '               ^\n'
            "LanguageError: returning 'i64' from a function with return "
            "type 'string'\n")

    # ToDo
    def test_compare_i64_and_bool(self):
        return
        with self.assertRaises(Exception) as cm:
            transpile_source('def foo() -> bool:\n'
                             '    return 1 == True')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 1\n'
            '        return 1 == True\n'
            '               ^\n'
            "LanguageError: can't compare 'i64' and 'bool'\n")

    # ToDo
    def test_return_bool_from_function_returning_string(self):
        return
        with self.assertRaises(Exception) as cm:
            transpile_source('class Gam:\n'
                             '    value: bool\n'
                             'class Fam:\n'
                             '    gams: [Gam] = [Gam()]\n'
                             'class Foo:\n'
                             '    def fam() -> Fam:\n'
                             '        return Fam()\n'
                             'class Bar:\n'
                             '    foo: Foo = Foo()\n'
                             'def foo() -> string:\n'
                             '    return Bar().foo.fam().gams[0].value')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 11\n'
            '        return Bar().foo.fam().gams[0].value\n'
            '               ^\n'
            "LanguageError: returning 'bool' from a function with return "
            "type 'string'\n")

    # ToDo
    def test_using_class_member_that_does_not_exist(self):
        return
        with self.assertRaises(Exception) as cm:
            transpile_source('class Gam:\n'
                             '    value: bool\n'
                             'class Fam:\n'
                             '    gams: [Gam] = [Gam()]\n'
                             'class Foo:\n'
                             '    def fam() -> Fam:\n'
                             '        return Fam()\n'
                             'class Bar:\n'
                             '    foo: Foo = Foo()\n'
                             'def foo() -> string:\n'
                             '    return Bar().foo.fam().fams[0].value')

        self.assertEqual(
            remove_ansi(str(cm.exception)),
            '  File "", line 11\n'
            '        return Bar().foo.fam().kams[0].value\n'
            '                               ^\n'
            "LanguageError: 'Fam' has no member 'kams'\n")
