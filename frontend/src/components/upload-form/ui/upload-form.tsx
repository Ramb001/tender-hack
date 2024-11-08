import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { formSchema } from "../model/upload-form-schema";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useUploadUrlMutation } from "../api/upload-api";
import { Button } from "@/components/ui/button";
export const UploadForm = () => {
  const [uploadUrl] = useUploadUrlMutation();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });
  function onSubmit(values: z.infer<typeof formSchema>) {
    uploadUrl({ url: values.url });
  }
  return (
    <Form {...form}>
      <form
        className="border p-4 rounded-xl grid gap-6 "
        onSubmit={form.handleSubmit(onSubmit)}
      >
        <FormField
          control={form.control}
          name="url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Вставьте ссылку на сессию</FormLabel>
              <FormControl>
                <Input
                  placeholder="Вставтье ссылку на сессию"
                  type="url"
                  {...field}
                />
              </FormControl>
            </FormItem>
          )}
        />
        <Button>Отправить</Button>
      </form>
    </Form>
  );
};
