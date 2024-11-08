import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { formSchema, options } from "../model/upload-form-schema";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useUploadUrlMutation } from "../api/upload-api";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { cn } from "@/lib/utils";
import { LoaderIcon } from "lucide-react";

export const UploadForm = () => {
  const { toast } = useToast();
  const [uploadUrl, { isSuccess, isError, isLoading }] = useUploadUrlMutation();
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      urls: "",
      options: ["recents", "home"],
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    // Разделяем строки на массив ссылок

    uploadUrl({ url: values.urls })
      .unwrap()
      .then(() =>
        toast({
          variant: "default",
          title: "Ссылки успешно отправлены",
        })
      )
      .catch(() =>
        toast({
          variant: "destructive",
          title: "Произошла ошибка, попробуйте еще раз",
        })
      );

    // if (isError) {
    // }
    // if (isSuccess) {
    // }
  }

  return (
    <Form {...form}>
      <form
        className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md border border-gray-300 space-y-6"
        onSubmit={form.handleSubmit(onSubmit)}
      >
        <FormField
          control={form.control}
          name="urls"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="text-lg font-semibold">
                Вставьте ссылки на сессии
              </FormLabel>
              <FormControl>
                <Textarea
                  className="resize-none p-3 rounded-md border-gray-300 focus:ring focus:ring-blue-200"
                  rows={4}
                  placeholder="Вставьте ссылки, разделенные новой строкой"
                  {...field}
                />
              </FormControl>
              <FormDescription className="text-sm text-gray-500 mt-1">
                Каждая ссылка должна быть на новой строке.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <Dialog>
          <DialogTrigger asChild>
            <Button className="w-full py-2 bg-blue-600 text-white rounded-md shadow hover:bg-blue-500 transition duration-200">
              Пункты для проверки
            </Button>
          </DialogTrigger>
          <DialogContent className="p-6 rounded-lg border-gray-300">
            <FormField
              control={form.control}
              name="options"
              render={() => (
                <FormItem>
                  <div className="mb-4">
                    <FormLabel className="text-lg font-semibold">
                      Выберите пункты проверки
                    </FormLabel>
                    <FormDescription className="text-sm text-gray-500 mt-1">
                      После выбора нажмите отправить
                    </FormDescription>
                  </div>

                  <div className="space-y-3">
                    {options.map((item) => (
                      <FormField
                        key={item.id}
                        control={form.control}
                        name="options"
                        render={({ field }) => {
                          return (
                            <FormItem
                              key={item.id}
                              className="flex items-center space-x-3"
                            >
                              <FormControl>
                                <Checkbox
                                  checked={field.value?.includes(item.id)}
                                  onCheckedChange={(checked) => {
                                    return checked
                                      ? field.onChange([
                                          ...field.value,
                                          item.id,
                                        ])
                                      : field.onChange(
                                          field.value?.filter(
                                            (value) => value !== item.id
                                          )
                                        );
                                  }}
                                />
                              </FormControl>
                              <FormLabel className="font-normal text-gray-700">
                                {item.label}
                              </FormLabel>
                            </FormItem>
                          );
                        }}
                      />
                    ))}
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
          </DialogContent>
        </Dialog>

        <Button
          className={cn(
            "w-full py-2 bg-blue-600 text-white rounded-md shadow hover:bg-blue-500 transition duration-200"
          )}
          type="submit"
        >
          {isLoading ? <LoaderIcon className="animate-spin" /> : "Отправить"}
        </Button>
      </form>
    </Form>
  );
};
