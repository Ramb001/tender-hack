import { z } from "zod";
export const options = [
  {
    id: "name",
    label: "Наименование",
  },
  {
    id: "Contract",
    label: "Обеспечение исполнения контракта",
  },
  {
    id: "lisence",
    label: "Наличие сертификатов/лицензий",
  },
  {
    id: "delivery",
    label: "График поставок",
  },
  {
    id: "price",
    label: "Максимальное значение цены контракта / Начальная цена",
  },
  {
    id: "characteristics",
    label: "Характеристики",
  },
] as const;

export const formSchema = z.object({
  file: z.instanceof(File).optional(),
  urls: z.string().url({ message: "Формат должен быть в виде ссылке" }),
  options: z.array(z.string()).refine((value) => value.some((item) => item), {
    message: "Вы должны выбрать пункты для проверки",
  }),
});
