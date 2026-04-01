import React from 'react';
import Test from "./component/Test/Test";

const text = `Hello World\nNext line\nTab\tindent`;
export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
        <Test></Test>
    </div>
  );
}
