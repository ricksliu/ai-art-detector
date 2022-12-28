export interface RequestImage {
  image: string;
  filename: string;
  url?: string;
  timestamp?: Date;
  is_ai_generated?: boolean;
}

export interface RequestImageArray extends Array<RequestImage> { }
