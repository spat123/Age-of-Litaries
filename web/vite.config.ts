import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

// Обычная сборка: npm run build. Сборка одним файлом для показа: npm run single
// (кладёт всю игру в refs/igra.html вместе с картинками).
export default defineConfig(({ mode }) => ({
  base: "./",
  server: { fs: { allow: [".."] } },
  plugins: mode === "single" ? [viteSingleFile()] : [],
  build:
    mode === "single"
      ? { outDir: "dist-single", assetsInlineLimit: 100_000_000, chunkSizeWarningLimit: 50_000 }
      : { outDir: "dist", chunkSizeWarningLimit: 5_000 },
}));
