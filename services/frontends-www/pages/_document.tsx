import Document, { Html, Main, NextScript, DocumentContext, DocumentInitialProps } from "next/document";
import React from "react";
import { ServerStyleSheet } from "styled-components";

export default class MarkDocument extends Document {
  // To avoid FOUC: https://github.com/vercel/next.js/blob/canary/examples/with-styled-components-babel/pages/_document.tsx
  static async getInitialProps(ctx: DocumentContext): Promise<DocumentInitialProps> {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;
    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) => sheet.collectStyles(<App {...props} />),
        });
      const initialProps = await Document.getInitialProps(ctx);
      return {
        ...initialProps,
        styles: [
          <>
            {initialProps.styles}
            {sheet.getStyleElement()}
          </>,
        ],
      };
    } finally {
      sheet.seal();
    }
  }

  render() {
    return (
      <Html>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
