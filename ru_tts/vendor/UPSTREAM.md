# Vendored Native Dependencies

## ru_tts

- Repository: https://github.com/poretsky/ru_tts
- Version: v6.3.3
- Commit: `2848d2892097320ed37fc963b439b15803f47f0c`
- Vendored path: upstream `src/` copied to `ru_tts/`

`ru_tts/config.h` is maintained locally because this project compiles the shared
library directly and does not run the upstream Autoconf configuration step.

## Sonic

- Repository used by ru_tts-for-nvda: https://gitverse.ru/kvark128/sonic
- Commit: `b93885dcb70aae50c6f76b0fe4e0868f029a077e`
- Vendored files: `sonic/sonic.c` and `sonic/sonic.h`

Only the classic Sonic C implementation used by the local bridge is included.
