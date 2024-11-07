import Head from 'expo-router/head';
import { Tabs } from "expo-router";

export default function RootLayout() {
  return (
    <>
      <Head>
        <title>Patent Checker</title>
      </Head>
      <Tabs>
        <Tabs.Screen name="index" options={{ title: "Checker" }}/>
        <Tabs.Screen name="searcher" options={{ title: "Searcher" }}/>
      </Tabs>
    </>

  );
}
