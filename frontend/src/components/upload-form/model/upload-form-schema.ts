import { z } from "zod";
export const formSchema = z.object({
  file: z.instanceof(File),
  url: z.string(),
});
