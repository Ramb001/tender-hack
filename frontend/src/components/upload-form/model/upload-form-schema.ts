import { z } from "zod";

// Схема для одного URL
export const formSchemaSingle = z.object({
  url: z
    .string()
    .url("Введите корректный URL") // Проверка на корректный URL
    .nonempty("Поле не может быть пустым"), // Поле обязательно
});

// Схема для списка URL
export const formSchemaList = z.object({
  urls: z
    .array(z.string().url("Некорректный URL")) // Проверка на массив URL
    .nonempty("Введите хотя бы одну ссылку"), // Поле обязательно, массив не может быть пустым
});
