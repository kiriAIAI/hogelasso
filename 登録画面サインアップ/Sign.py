import * as React from "react";

function MyComponent() {
  return (
    <div className="pt-14 pb-7 pl-16 bg-white max-w-[960px] rounded-[30px] max-md:pl-5">
      <div className="flex gap-5 max-md:flex-col max-md:gap-0">
        <div className="flex flex-col w-[42%] max-md:ml-0 max-md:w-full">
          <div className="flex flex-col grow max-md:mt-10">
            <div className="flex gap-5 px-px w-full">
              <div className="flex-auto text-3xl font-bold text-black">
                サインアップ
              </div>
              <div className="flex gap-2 self-start mt-1">
                <img
                  loading="lazy"
                  srcSet="..."
                  className="shrink-0 aspect-[0.89] w-[25px]"
                />
                <img
                  loading="lazy"
                  srcSet="..."
                  className="shrink-0 self-start w-5 aspect-square"
                />
              </div>
            </div>
            <div className="mt-8 text-xl text-black">ユーザー名</div>
            <div className="flex gap-5 justify-between px-5 py-2 mt-3.5 text-base font-bold whitespace-nowrap bg-white rounded-md border border-solid shadow-sm border-neutral-200 text-neutral-200">
              <div className="my-auto">username</div>
              <img
                loading="lazy"
                srcSet="..."
                className="shrink-0 aspect-square w-[25px]"
              />
            </div>
            <div className="mt-10 text-xl text-black">メールアドレス</div>
            <div className="flex gap-5 px-5 py-2 mt-4 text-base font-bold whitespace-nowrap bg-white rounded-md border border-solid shadow-sm border-neutral-200 text-neutral-200">
              <div className="flex-auto">example@gmail.com</div>
              <img
                loading="lazy"
                srcSet="..."
                className="shrink-0 aspect-square w-[25px]"
              />
            </div>
            <div className="mt-9 text-xl text-black">パスワード</div>
            <div className="flex gap-5 justify-between px-5 py-2 mt-4 text-base font-bold whitespace-nowrap bg-white rounded-md border border-solid shadow-sm border-neutral-200 text-neutral-200">
              <div className="my-auto">**********</div>
              <img
                loading="lazy"
                srcSet="..."
                className="shrink-0 aspect-square w-[25px]"
              />
            </div>
            <div className="mt-9 text-xl text-black">パスワード再確認</div>
            <div className="flex gap-5 justify-between px-5 py-2 mt-3.5 text-base font-bold whitespace-nowrap bg-white rounded-md border border-solid shadow-sm border-neutral-200 text-neutral-200">
              <div className="my-auto">**********</div>
              <img
                loading="lazy"
                srcSet="..."
                className="shrink-0 aspect-square w-[25px]"
              />
            </div>
            <div className="self-center mt-3.5 text-base font-bold text-stone-400">
              既にアカウントをお持ちの方
            </div>
            <div className="justify-center items-center px-16 py-3.5 mt-5 text-2xl font-bold text-white whitespace-nowrap bg-orange-500 rounded-xl max-md:px-5">
              サインアップ
            </div>
          </div>
        </div>
        <div className="flex flex-col ml-5 w-[58%] max-md:ml-0 max-md:w-full">
          <img
            loading="lazy"
            src="https://cdn.builder.io/api/v1/image/assets/TEMP/cae351fa1dc6aecdbd071b33ce6da00f44044830f6ad6a9157940d0f63565365?"
            className="self-stretch my-auto w-full aspect-[1.09] max-md:mt-10 max-md:max-w-full"
          />
        </div>
      </div>
    </div>
  );
}

