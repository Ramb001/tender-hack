import { z } from "zod";
export const options = [
  {
    id: "recents",
    label: "Recents",
  },
  {
    id: "home",
    label: "Home",
  },
  {
    id: "applications",
    label: "Applications",
  },
  {
    id: "desktop",
    label: "Desktop",
  },
  {
    id: "downloads",
    label: "Downloads",
  },
  {
    id: "documents",
    label: "Documents",
  },
] as const;

export const formSchema = z.object({
  file: z.instanceof(File).optional(),
  urls: z.string().url({ message: "Формат должен быть в виде ссылке" }),
  options: z.array(z.string()).refine((value) => value.some((item) => item), {
    message: "Вы должны выбрать пункты для проверки",
  }),
});
