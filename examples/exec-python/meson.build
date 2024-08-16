project(
    'netstring',
    'c',
    version: '0.1.0',
    default_options: ['warning_level=3'],
)

py = import('python').find_installation(pure: false)

install_subdir('src/netstring', install_dir: py.get_install_dir())

gen_cffi_src = find_program('gen-cffi-src')

netstring = subproject('netstring-c')
netstring_dep = netstring.get_variable('netstring_c_dep')

netstring_ext_src = custom_target(
    command: [
        gen_cffi_src,
        'exec-python',
        '@INPUT@',
        '@OUTPUT@',
    ],
    output: '_netstring.c',
    input: [
        'cffi/netstring/_netstring.c.py'
    ],
)

py.extension_module(
    '_netstring',
    netstring_ext_src,
    subdir: 'netstring',
    install: true,
    dependencies: [netstring_dep, py.dependency()],
    limited_api: '3.8',
)
