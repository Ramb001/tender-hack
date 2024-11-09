import { z } from "zod";
export const options = [
  {
    id: "1",
    label: "Наименование",
  },
  {
    id: "2",
    label: "Обеспечение исполнения контракта",
  },
  {
    id: "3",
    label: "Наличие сертификатов/лицензий",
  },
  {
    id: "4",
    label: "График поставок",
  },
  {
    id: "5",
    label: "Максимальное значение цены контракта / Начальная цена",
  },
  {
    id: "6",
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
