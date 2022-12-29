export interface RequestImage {
  image: ArrayBuffer;
  filename: string;
  url?: string;
  timestamp?: Date;
  is_ai_generated?: boolean;
}

export interface RequestImageArray extends Array<RequestImage> { }
