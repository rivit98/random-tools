//
// Ent -  Entropy Level and FPU Density Measurement Tool
// code by gynvael.coldwind//vx and j00ru//vx
// mailto: gynvael@coldwind.pl or j00ru@vexillium.org
// www   : http://vexillium.org
//         http://gynvael.coldwind.pl
//
// CHANGELOG
// 
// 0.0.2 -> 0.0.3 (current)
// * Rewritten parts of the code
// * Switched from TGA to PNG
// * Commented stuff
// * Removed dependency from my personal libs
// * Added a few checks here and there
// * The code is more readable
//
// 0.0.1 -> 0.0.2
// * Added FPU Density Scan in PE files
// * Scaled down the height to 480
//
// 0.0.1
// * Initial Version
//
//
// LICENSE
// Permission is hereby granted to use, copy, modify, and distribute this
// source code, or portions hereof, for any purpose, without fee, subject
// to the following restrictions:
// 
// 1. The origin of this source code must not be misrepresented.
// 
// 2. Altered versions must be plainly marked as such and must not
//    be misrepresented as being the original source.
// 
// 3. This Copyright notice may not be removed or altered from any
//    source or altered source distribution. 
// 
// This software is provided AS IS. The author does not guarantee that 
// this program works, is bugfree, etc. The author does not take any
// responsibility for eventual damage caused by this program.
// Use at own risk.
//

// Includes
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <windows.h>
#include <png.h>

// Namespace
using namespace std;

// Config stuff
#define VERSION "0.0.3"
#define CHART_HEIGHT 480
#define BAR_HEIGHT    20

// Function declarations
static unsigned char * FileGetContent(const char *FileName, size_t *Size);
static void MakeHistogram(const unsigned char *Data, int Size, int Array[256]);
static double GetEntropy(const unsigned char *Data, int Size);
static void WritePNGErrorHandler(png_structp png_ptr, png_const_charp msg);

// Main function
int
main(int argc, char **argv)
{
  // Some variables
  int SampleLength = 256;
  size_t height = CHART_HEIGHT + BAR_HEIGHT;
  size_t width;
  unsigned char *raw, *all;

  // Show banner
  puts("Ent v." VERSION ", an entropy level and FPU density measurement tool\n"
       "                         by gynvael.coldwind//vx and j00ru//vx\n");

  // Check the arguments
  if(argc < 2)
  {
    // Show usage and quit
    printf("usage: ent <FileName> [<SampleLength>]\n"
           "SampleLength is 256 bytes by default\n");
    return 1;
  }

  // Any non-standard sample length?
  if(argc == 3)
    SampleLength = atoi(argv[2]);

  // Load the file into memory
  unsigned char *data;
  size_t s, i, sz;

  data = FileGetContent(argv[1], &s);
  if(data == NULL)
  {
    fprintf(stderr, "file not found\n");
    return 2;
  }

  // Allocate space for the chart bitmap
  sz = s - SampleLength;
  width = s / SampleLength;

  all = new unsigned char[width * height * 3];
  raw = all;

  // Paint it white
  memset(raw, 0xff, width * height * 3);

  // Some variables
  size_t j, cnt = 0;

  printf("Calculating entropy...");

  // Calculate and draw the main entropy
  for(i = 0; i < sz; i += SampleLength, cnt++)
  {
    // Some variables
    size_t hi;

    // Calculate the entropy
    double ent = GetEntropy(&data[i], SampleLength);
    ent /= SampleLength;
    ent = 1.0 - ent;
    ent *= ent; // Square scale
    ent *= 100.0;
    hi = CHART_HEIGHT - (int)(ent * ((float)(CHART_HEIGHT - 1) / 100.0f));

    printf("\rCalculating entropy... [Fent(%.8Xh - %.8Xh) = %3i%%]",
        i, i + SampleLength - 1, (int)ent);

    // Precalculate some parts of the color
    int ent_by_100 = (int)(ent * (255.0 / 100.0));
    int ent_by_120 = (int)(ent * (255.0 / 120.0));
    int ent_by_200 = (int)(ent * (255.0 / 200.0));

    // Draw the chart
    for(j = CHART_HEIGHT + BAR_HEIGHT - 1; j >= hi + BAR_HEIGHT; j--)
    {
      if(j - BAR_HEIGHT <= 13)
      {
        // Very high entropy
        raw[(cnt + j * width) * 3 + 2] = 0x00;
        raw[(cnt + j * width) * 3 + 1] = 0x00;
        raw[(cnt + j * width) * 3 + 0] = ent_by_100;
      }
      else if(j - BAR_HEIGHT <= 92)
      {
        // High entropy
        raw[(cnt + j * width) * 3 + 2] = 0x00;
        raw[(cnt + j * width) * 3 + 1] = ent_by_120;
        raw[(cnt + j * width) * 3 + 0] = ent_by_120;
      }
      else if(j - BAR_HEIGHT <= 192)
      {
        // Average entropy
        raw[(cnt + j * width) * 3 + 2] = 0x00;
        raw[(cnt + j * width) * 3 + 1] = ent_by_100;
        raw[(cnt + j * width) * 3 + 0] = 0x00;
      }
      else
      {
        // Low entropy
        raw[(cnt + j * width) * 3 + 2] = ent_by_200;
        raw[(cnt + j * width) * 3 + 1] = 0x00;
        raw[(cnt + j * width) * 3 + 0] = ent_by_200;
      }
    } // for
  } // for

  // Skip to next line
  putchar('\n');

  // Now, draw the sections if this is a PE file
  while(*(short*)data == *(short*)"MZ")
  {
    // Some info
    puts("PE File found, scanning code section for FPU instructions...");

    // Header
    IMAGE_DOS_HEADER *DosHeader = (IMAGE_DOS_HEADER*)data;

    if(DosHeader->e_lfanew + sizeof(IMAGE_NT_HEADERS) >= s)
    {
      fprintf(stderr, "error: not a PE file after all, skipping FPU density scan\n");
      break;
    }

    IMAGE_NT_HEADERS *NtHeaders = (IMAGE_NT_HEADERS*)(data + DosHeader->e_lfanew);

    // Check magic
    if(NtHeaders->Signature != IMAGE_NT_SIGNATURE)
    {
      fprintf(stderr, "error: PE sig does not match, not a PE file after all, skipping FPU scan\n");
      break;
    }

    // Check the section sanity
    if(DosHeader->e_lfanew + sizeof(IMAGE_NT_HEADERS) +
       NtHeaders->FileHeader.NumberOfSections * sizeof(IMAGE_SECTION_HEADER) >= s)
    {
      fprintf(stderr, "error: PE sections are invalid, skipping FPU scan\n");
      break;
    }
    
    // Draw grey bar
    for(j = 0; j < BAR_HEIGHT; j++)
      for(i = 0; i < width; i++)
      {
        raw[(i + j * width) * 3 + 2] = 0xA0;
        raw[(i + j * width) * 3 + 1] = 0xA0;
        raw[(i + j * width) * 3 + 0] = 0xA0;
      }

    // Now for the sections
    IMAGE_SECTION_HEADER *Section = (IMAGE_SECTION_HEADER*)(NtHeaders + 1);
    int k;
    for(k = 0; k < NtHeaders->FileHeader.NumberOfSections; k++)
    {
      unsigned int st, end;
      st = Section[k].PointerToRawData / 256;
      end = (Section[k].PointerToRawData+Section[k].SizeOfRawData) / 256;
      if(st >= (unsigned)width) st = width - 1;
      if(end >= (unsigned)width) end = width - 1;

      int color[3] = { 0xA0, 0x40, 0x00 };

      // Code section?
      if((Section[k].Characteristics & IMAGE_SCN_CNT_CODE) ||
         (Section[k].Characteristics & IMAGE_SCN_MEM_EXECUTE))
      {
        color[0] = 0; color[1] = 0xff; color[2] = 0;
      }
      // Data section ?
      else if(Section[k].Characteristics & IMAGE_SCN_CNT_INITIALIZED_DATA)
      {
        color[0] = 0; color[1] = 0; color[2] = 0xff;
      }
      // Uninit Data section ?
      else if(Section[k].Characteristics & IMAGE_SCN_CNT_UNINITIALIZED_DATA)
      {
        color[0] = 0; color[1] = 0; color[2] = 0x80;
      }
      // Unknown but write?
      else if(Section[k].Characteristics & IMAGE_SCN_MEM_WRITE)
      {
        color[0] = 0x80; color[1] = 0; color[2] = 0;
      }
      // Unknown but read?
      else if(Section[k].Characteristics & IMAGE_SCN_MEM_WRITE)
      {
        color[0] = 0; color[1] = 0x80; color[2] = 0x80;
      }

      // Draw
      for(j = 0; j < 20; j++)
        for(i = st; i <= end; i++)
        {
          // Draw bar
          raw[(i + j * width) * 3 + 0] = color[0];
          raw[(i + j * width) * 3 + 1] = color[1];
          raw[(i + j * width) * 3 + 2] = color[2];
        }

      // Is this a code section ?
      if((Section[k].Characteristics & IMAGE_SCN_CNT_CODE) ||
         (Section[k].Characteristics & IMAGE_SCN_MEM_EXECUTE))
      {
        // Scan for FPU
        for(i = st; i < end; i++)
        {
          // Some variable
          size_t PossibleFPUCount = 0;

          // Any FPU instruction?
          for(j = i*256; j < (i+1)*256; j++)
            if((unsigned char)data[j] >= 0xD8 && (unsigned char)data[j] <= 0xDF) // Is FPU?
              PossibleFPUCount++;

          PossibleFPUCount *= 2;

          PossibleFPUCount = (PossibleFPUCount * 19) / 256;

          if(PossibleFPUCount > 19) PossibleFPUCount = 19;

          // Draw the FPU chart
          for(j = 19; j > 19 - PossibleFPUCount; j--)
          {
            // Draw pixel
            raw[(i + j * width) * 3 + 2] = 0;
            raw[(i + j * width) * 3 + 1] = 0;
            raw[(i + j * width) * 3 + 0] = 0xff;
          }
        }
      }
    }

    // Done
    break;
  }

  // Delete the file data
  free(data);

  // Setup then name of the output file
  char name[512];
  snprintf(name, sizeof(name), "%s.png", argv[1]);

  // Open the file
  FILE *f = fopen(name, "wb");
  if(!f)
  {
    // Write an error and quit
    fprintf(stderr, "error: could not create output file \"%s\"\n", name);
    return 1;
  }

  // Some PNG variables
  png_structp png_ptr;
  png_infop info_ptr;
  png_bytep row_pointers[CHART_HEIGHT + BAR_HEIGHT];

  // Setup the row_pointers array
  for(i = 0; i < CHART_HEIGHT + BAR_HEIGHT; i++)
    row_pointers[i] = (png_bytep)&raw[i * width * 3];

  // Create the write struct
  png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, WritePNGErrorHandler, NULL);
  if(!png_ptr)
  {
    // Write an error and quit
    fprintf(stderr, "error: create PNG write struct failed\n", name);
    return 2;
  }

  // Create info pointer
  info_ptr = png_create_info_struct(png_ptr);
  if(!info_ptr)
  {
    // Write an error and quit
    fprintf(stderr, "error: create PNG info struct\n", name);
    return 3;
  }

  // Setup comment
#ifndef PLZ_DO_NOT_INCLUDE_THIS_BANNER_PLZ_PLZ_PLZ_K_THX
  png_text_struct text_str;
  memset(&text_str, 0, sizeof(text_str));
  text_str.compression = -1; // tEXt, none
  text_str.key = "Made by Ent v."VERSION" by gynvael.coldwind//vx and j00ru//vx";
  text_str.text = "\r\nEnt - Entropy Level and FPU Density Measurement Tool\r\n"
                  "code by gynvael.coldwind//vx and j00ru//vx\r\n"
                  "mailto: gynvael@coldwind.pl or j00ru@vexillium.org\r\n"
                  "www   : http://vexillium.org\r\n"
                  "        http://gynvael.coldwind.pl\r\n";
  text_str.text_length = strlen(text_str.text);

  // Add comment to info
  info_ptr->num_text = 1;
  info_ptr->max_text = 1;
  info_ptr->text = &text_str;
#endif
   
  // Setup the jump  
  if(setjmp(png_jmpbuf(png_ptr)))
  {
    // Write an error and quit
    fprintf(stderr, "error: PNG error (details follow)\n", name);
    return 4;
  }

  // Write the PNG
  png_init_io(png_ptr, f);
  png_set_IHDR(png_ptr, info_ptr, width, height,
               8, PNG_COLOR_TYPE_RGB, PNG_INTERLACE_NONE,
               PNG_COMPRESSION_TYPE_BASE, PNG_FILTER_TYPE_BASE);
  png_write_info(png_ptr, info_ptr);
  png_write_image(png_ptr, row_pointers);
  png_write_end(png_ptr, NULL);

  // Close the file
  fclose(f);

  // Free the memory
  delete all;

  // It's done.
  puts("Done.");

  // Done
  return 0;
}

//
// FileGetContent
//
static unsigned char *
FileGetContent(const char *FileName, size_t *Size)
{
  // Some variables
  FILE *f;
  size_t FileSize;
  unsigned char *Data;

  // Open the file
  f = fopen(FileName, "rb");
  if(!f)
    return NULL;

  // Get file size
  fseek(f, 0, SEEK_END);
  FileSize = ftell(f);
  fseek(f, 0, SEEK_SET);

  // Allocate memory
  Data = (unsigned char*)malloc(FileSize + 1);
  if(!Data)
  {
    fclose(f);
    return NULL;
  }

  // Read file content
  FileSize = fread(Data, 1, FileSize, f);
  Data[FileSize] = 0;

  // Close the file
  fclose(f);

  // Return
  if(Size) // Size is optional
    *Size = FileSize;
  return Data;
}

//
// MakeHistogram Function
//
static void
MakeHistogram(const unsigned char *Data, int Size, int Array[256])
{
  // Some variable
  int i;

  // Zero it!
  memset(Array, 0, sizeof(int) * 256);

  // Fill the array
  for(i = 0; i < Size; i++)
    Array[Data[i]]++;
}

//
// GetEntropy Function
//
static double
GetEntropy(const unsigned char *Data, int Size)
{
  // Some variables
  int Array[256];
  int i;
  double Entropy = 0.0;

  // Create the histogram
  MakeHistogram(Data, Size, Array);

  // Calculate the entropy
  for(i = 0; i < 256; i++)
  {
    double Pr = (double)Array[i] / Size;
    Entropy += Pr * (double)Array[i];
  }

  // Return the entropy
  return Entropy; 
}

//
// WritePNGErrorHandler Function
//
static void WritePNGErrorHandler(png_structp png_ptr, png_const_charp msg)
{
  // Unused
  (void)png_ptr;

  // Write the error to stderr
  fprintf(stderr, "error: %s (PNG write)\n", msg);

  // "Eject! EJECT!"
  exit(1);
}

